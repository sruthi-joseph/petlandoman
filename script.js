/**
 * Petland Oman - Core JavaScript Controller
 * Implements: Sticky Header, Mobile Navigation, Smooth Video Scroll-Seeking,
 * Infinite Marquee Speeds, Popups, and Contact Form routing.
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initMobileNav();
    initCanvasScrollSeek();
    initBannerSlideshow();
    initModals();
    initContactForm();
    initHeroLogoOverlay();
    initMobileCarousels();
});

/* ==========================================================================
   1. HEADER & NAVIGATION
   ========================================================================== */
function initHeader() {
    const header = document.getElementById('main-header');
    if (!header) return;

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    }, { passive: true });
}

function initMobileNav() {
    const toggle = document.getElementById('nav-toggle');
    const menu = document.getElementById('nav-menu');
    if (!toggle || !menu) return;

    toggle.addEventListener('click', () => {
        menu.classList.toggle('active');
        const icon = toggle.querySelector('i');
        if (menu.classList.contains('active')) {
            icon.className = 'fa-solid fa-xmark';
        } else {
            icon.className = 'fa-solid fa-bars';
        }
    });

    // Close menu when clicking links
    menu.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            menu.classList.remove('active');
            toggle.querySelector('i').className = 'fa-solid fa-bars';
        });
    });
}

/* ==========================================================================
   2. SMOOTH CANVAS SCROLL-SEEK ANIMATION
   ========================================================================== */
class CanvasScrollScrubber {
    constructor(containerId, canvasId, frameCount) {
        this.container = document.getElementById(containerId);
        this.canvas    = document.getElementById(canvasId);
        if (!this.container || !this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        this.overlay = document.getElementById('hero-logo-overlay');

        // Detect mobile viewport (768px or below)
        this.isMobile  = window.innerWidth <= 768;
        this.frameCount = this.isMobile ? 211 : frameCount; // 211 mobile / 169 desktop

        this.images = [];
        this.loadedIndices = [];
        this.loadingPromises = new Map();

        // --- Scroll state ---
        this.currentProgress = 0;
        this.targetProgress  = 0;
        this.lerpFactor      = this.isMobile ? 1 : 0.12; // 1 = no easing on mobile

        this.lastRenderedFrame = -1;
        this.rafScheduled      = false; // tracks if tick loop is currently running

        // Cached positions to prevent layout thrashing (getBoundingClientRect)
        this.containerTop      = 0;
        this.totalScrollable   = 0;

        this.init();
    }

    init() {
        this.updateLayoutMetrics();
        window.addEventListener('resize', () => {
            this.updateLayoutMetrics();
            this.resizeCanvas();
        }, { passive: true });

        // Apply GPU acceleration hint to canvas on mobile
        if (this.isMobile) {
            this.canvas.style.willChange   = 'transform';
            this.canvas.style.transform    = 'translateZ(0)';
            this.canvas.style.backfaceVisibility = 'hidden';
        }

        this.preloadImages();

        // Scroll listener: passive, avoids layout thrashing, schedules rAF dynamically
        window.addEventListener('scroll', () => {
            this.handleScroll();
            if (!this.rafScheduled) {
                this.rafScheduled = true;
                requestAnimationFrame(() => this.tick());
            }
        }, { passive: true });
    }

    updateLayoutMetrics() {
        // Absolute container top offset relative to the document
        let el = this.container;
        let top = 0;
        while (el) {
            top += el.offsetTop;
            el = el.offsetParent;
        }
        this.containerTop = top;
        this.totalScrollable = this.container.offsetHeight - window.innerHeight;
    }

    resizeCanvas() {
        // Cap DPR at 2 on mobile to save GPU bandwidth
        const dpr = this.isMobile
            ? Math.min(window.devicePixelRatio || 1, 2)
            : (window.devicePixelRatio || 1);

        this.canvas.width  = window.innerWidth  * dpr;
        this.canvas.height = window.innerHeight * dpr;

        if (this.lastRenderedFrame !== -1) {
            this.drawFrame(this.lastRenderedFrame);
        }
    }

    getFramePath(index) {
        const pad = String(index).padStart(3, '0');
        const pathPrefix = window.location.pathname.includes('/pages/') ? '../' : '';
        const dir = this.isMobile
            ? 'assets/frames/hero_mobile'
            : 'assets/frames/hero_desktop';
        return `${pathPrefix}${dir}/ezgif-frame-${pad}.png`;
    }

    loadImage(index) {
        if (this.images[index]) return Promise.resolve(true);
        if (this.loadingPromises.has(index)) return this.loadingPromises.get(index);

        const promise = new Promise((resolve) => {
            const img = new Image();
            img.onload = () => {
                const proceed = () => {
                    this.images[index] = img;
                    this.loadingPromises.delete(index);
                    
                    // Insert into loadedIndices in sorted order if not present
                    if (!this.loadedIndices.includes(index)) {
                        const pos = this.loadedIndices.findIndex(idx => idx > index);
                        if (pos === -1) {
                            this.loadedIndices.push(index);
                        } else {
                            this.loadedIndices.splice(pos, 0, index);
                        }
                    }

                    // If this is the active frame, redraw immediately
                    const currentNeededFrame = Math.min(
                        this.frameCount,
                        Math.max(1, Math.round(this.currentProgress * (this.frameCount - 1) + 1))
                    );
                    if (index === currentNeededFrame) {
                        this.drawFrame(currentNeededFrame);
                        this.lastRenderedFrame = currentNeededFrame;
                    }
                    resolve(true);
                };

                // Asynchronously decode image off the main thread before drawing
                if (typeof img.decode === 'function') {
                    img.decode().then(proceed).catch(proceed);
                } else {
                    proceed();
                }
            };
            img.onerror = () => {
                this.loadingPromises.delete(index);
                resolve(false);
            };
            img.src = this.getFramePath(index);
        });

        this.loadingPromises.set(index, promise);
        return promise;
    }

    preloadImages() {
        // PRIORITY 1: Frame 1 → immediate first paint
        this.loadImage(1).then(() => {
            this.drawFrame(1);
            this.lastRenderedFrame = 1;

            // PRIORITY 2: Frames 2-20 → fast early-scroll coverage
            const p2 = [];
            for (let i = 2; i <= Math.min(20, this.frameCount); i++) p2.push(this.loadImage(i));

            Promise.all(p2).then(() => {
                // PRIORITY 3: Sparse every-4th frame across the full sequence
                const p3 = [];
                for (let i = 24; i <= this.frameCount; i += 4) {
                    p3.push(this.loadImage(i));
                }

                Promise.all(p3).then(() => {
                    // PRIORITY 4: Fill all remaining frames
                    const remaining = [];
                    for (let i = 2; i <= this.frameCount; i++) {
                        if (!this.images[i] && !this.loadingPromises.has(i)) {
                            remaining.push(i);
                        }
                    }

                    const loaderCount = this.isMobile ? 4 : 6;
                    let ptr = 0;
                    const next = () => {
                        if (ptr >= remaining.length) return;
                        this.loadImage(remaining[ptr++]).then(next);
                    };
                    for (let i = 0; i < loaderCount; i++) next();
                });
            });
        });
    }

    handleScroll() {
        if (this.totalScrollable <= 0) return;
        const scrolled = window.scrollY - this.containerTop;
        let progress   = scrolled / this.totalScrollable;
        progress       = Math.min(Math.max(0, progress), 1);
        this.targetProgress = progress;
    }

    getNearestLoadedFrame(index) {
        if (this.images[index]) return this.images[index];
        if (this.loadedIndices.length === 0) return null;

        let low = 0;
        let high = this.loadedIndices.length - 1;

        while (low < high) {
            const mid = (low + high) >> 1;
            if (this.loadedIndices[mid] < index) {
                low = mid + 1;
            } else {
                high = mid;
            }
        }

        const val1 = this.loadedIndices[low];
        const val2 = low > 0 ? this.loadedIndices[low - 1] : val1;

        const diff1 = Math.abs(val1 - index);
        const diff2 = Math.abs(val2 - index);

        const nearestIdx = diff1 < diff2 ? val1 : val2;
        return this.images[nearestIdx];
    }

    evictExcessFrames(currentFrame) {
        const maxCacheSize = this.isMobile ? 50 : 100;
        if (this.loadedIndices.length <= maxCacheSize) return;

        // Sort copy of loadedIndices by their distance to currentFrame (descending)
        const sortedByDistance = [...this.loadedIndices]
            .filter(idx => idx !== 1) // Always keep frame 1
            .sort((a, b) => Math.abs(b - currentFrame) - Math.abs(a - currentFrame));

        const toEvictCount = this.loadedIndices.length - maxCacheSize;
        for (let i = 0; i < toEvictCount && i < sortedByDistance.length; i++) {
            const idxToEvict = sortedByDistance[i];
            this.images[idxToEvict] = null;
            
            const pos = this.loadedIndices.indexOf(idxToEvict);
            if (pos !== -1) {
                this.loadedIndices.splice(pos, 1);
            }
        }
    }

    tick() {
        // Calculate progress change
        let progressChanged = false;
        if (Math.abs(this.currentProgress - this.targetProgress) > 0.0001) {
            this.currentProgress += (this.targetProgress - this.currentProgress) * this.lerpFactor;
            progressChanged = true;
        } else if (this.currentProgress !== this.targetProgress) {
            this.currentProgress = this.targetProgress;
            progressChanged = true;
        }

        const frameIndex = Math.min(
            this.frameCount,
            Math.max(1, Math.round(this.currentProgress * (this.frameCount - 1) + 1))
        );

        if (frameIndex !== this.lastRenderedFrame) {
            this.drawFrame(frameIndex);
            this.lastRenderedFrame = frameIndex;
            this.evictExcessFrames(frameIndex);
        }

        // Keep loop running if we are still lerping or if progress hasn't stabilized
        const needsMoreTicks = Math.abs(this.currentProgress - this.targetProgress) > 0.0001;

        if (needsMoreTicks) {
            requestAnimationFrame(() => this.tick());
        } else {
            this.rafScheduled = false; // Stop the loop when idle
        }
    }

    drawFrame(index) {
        const img = this.getNearestLoadedFrame(index);
        if (!img) return;

        const w = this.canvas.width;
        const h = this.canvas.height;

        this.ctx.clearRect(0, 0, w, h);

        const iw = img.width;
        const ih = img.height;

        // Draw active logo overlay (integrated fade out)
        if (this.overlay) {
            const FADE_END = 0.30;
            const opacity = Math.max(0, 1 - (this.currentProgress / FADE_END));
            this.overlay.style.opacity = opacity;
        }

        if (this.isMobile) {
            // Mobile: object-fit contain with matching background
            const r  = Math.min(w / iw, h / ih);
            const nw = iw * r;
            const nh = ih * r;
            const x  = (w - nw) / 2;
            const y  = (h - nh) / 2;

            this.ctx.fillStyle = '#fdfdfd';
            this.ctx.fillRect(0, 0, w, h);
            this.ctx.drawImage(img, x, y, nw, nh);
        } else {
            // Desktop: object-fit cover
            const r = Math.min(w / iw, h / ih);
            let nw = iw * r;
            let nh = ih * r;
            let cx, cy, cw, ch, ar = 1;

            if (nw < w) ar = w / nw;
            if (Math.abs(ar - 1) < 1e-14 && nh < h) ar = h / nh;
            nw *= ar;
            nh *= ar;

            cw = iw / (nw / w);
            ch = ih / (nh / h);

            cx = (iw - cw) * 0.5;
            cy = (ih - ch) * 0.5;

            if (cx < 0) cx = 0;
            if (cy < 0) cy = 0;
            if (cw > iw) cw = iw;
            if (ch > ih) ch = ih;

            this.ctx.drawImage(img, cx, cy, cw, ch, 0, 0, w, h);
        }
    }
}

function initCanvasScrollSeek() {
    new CanvasScrollScrubber('scroll-canvas-section', 'scroll-animation-canvas', 169);
}

/* ==========================================================================
   3. BANNER SLIDESHOW  — runs continuously
   ========================================================================== */
function initBannerSlideshow() {
    const slides  = document.querySelectorAll('.banner-slide');
    const prevBtn = document.getElementById('banner-prev');
    const nextBtn = document.getElementById('banner-next');

    if (!slides.length) return;

    let current  = 0;
    const INTERVAL = 3000; // ms between slides

    function goTo(index) {
        slides[current].classList.remove('active');
        current = (index + slides.length) % slides.length;
        slides[current].classList.add('active');
    }

    // Arrow buttons (hidden but wired up for JS control)
    if (prevBtn) prevBtn.addEventListener('click', () => goTo(current - 1));
    if (nextBtn) nextBtn.addEventListener('click', () => goTo(current + 1));

    // Continuous auto-rotation — never stops
    setInterval(() => goTo(current + 1), INTERVAL);
}

/* ==========================================================================
   4. DETAILS POPUP MODALS
   ========================================================================== */
function initModals() {
    const modal = document.getElementById('details-modal');
    if (!modal) return;

    const backdrop = document.getElementById('modal-backdrop');
    const closeBtn = document.getElementById('modal-close');

    const modalImg = document.getElementById('modal-img-el');
    const modalTag = document.getElementById('modal-tag-el');
    const modalTitle = document.getElementById('modal-title-el');
    const modalPrice = document.getElementById('modal-price-el');
    const modalDesc = document.getElementById('modal-desc-el');
    const modalBtn = document.getElementById('modal-btn-el');
    const modalBenefitsList = document.getElementById('modal-benefits-list-el');

    // WhatsApp Contact Number
    const phoneNo = '96879260091';

    // Products Click Handlers
    document.querySelectorAll('.product-item').forEach(item => {
        item.addEventListener('click', () => {
            const name = item.getAttribute('data-name');
            const price = item.getAttribute('data-price');
            const image = item.getAttribute('data-image');
            const desc = item.getAttribute('data-description');
            
            modalImg.src = image;
            modalImg.alt = name;
            modalTag.textContent = 'Product';
            modalTitle.textContent = name;
            modalPrice.textContent = price;
            modalDesc.textContent = desc;

            // Hide benefits wrapper since it is a product
            const benefitsWrapper = modal.querySelector('.modal-benefits');
            if (benefitsWrapper) benefitsWrapper.style.display = 'none';

            // Configure WhatsApp order link
            const waMessage = `Hi Petland Oman, I'm interested in ordering the product: "${name}" (${price}). Please let me know the availability.`;
            modalBtn.href = `https://wa.me/${phoneNo}?text=${encodeURIComponent(waMessage)}`;
            modalBtn.innerHTML = 'Order on WhatsApp <i class="fa-brands fa-whatsapp"></i>';

            openModal();
        });
    });

    // Services Click Handlers
    document.querySelectorAll('.service-item').forEach(item => {
        item.addEventListener('click', () => {
            const name = item.getAttribute('data-name');
            const price = item.getAttribute('data-price');
            const image = item.getAttribute('data-image');
            const desc = item.getAttribute('data-description');
            const benefitsRaw = item.getAttribute('data-benefits') || '';
            
            modalImg.src = image;
            modalImg.alt = name;
            modalTag.textContent = 'Service Package';
            modalTitle.textContent = name;
            modalPrice.textContent = price;
            modalDesc.textContent = desc;

            // Populate benefits
            if (modalBenefitsList) {
                modalBenefitsList.innerHTML = '';
                const benefits = benefitsRaw.split(',');
                benefits.forEach(benefit => {
                    if (benefit.trim()) {
                        const li = document.createElement('li');
                        li.innerHTML = `<i class="fa-solid fa-circle-check"></i> ${benefit.trim()}`;
                        modalBenefitsList.appendChild(li);
                    }
                });
            }

            const benefitsWrapper = modal.querySelector('.modal-benefits');
            if (benefitsWrapper) benefitsWrapper.style.display = 'block';

            // Configure WhatsApp enquiry link
            const waMessage = `Hi Petland Oman, I would like to make an enquiry or booking for the service: "${name}". Please provide package options and available times.`;
            modalBtn.href = `https://wa.me/${phoneNo}?text=${encodeURIComponent(waMessage)}`;
            modalBtn.innerHTML = 'Send Enquiry on WhatsApp <i class="fa-brands fa-whatsapp"></i>';

            openModal();
        });
    });

    function openModal() {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Stop background scrolling
    }

    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = 'auto'; // Enable scrolling
    }

    closeBtn.addEventListener('click', closeModal);
    backdrop.addEventListener('click', closeModal);
    
    // Close with Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });
}

/* ==========================================================================
   5. CONTACT FORM SUBMISSION ROUTING
   ========================================================================== */
function initContactForm() {
    const form = document.getElementById('petland-contact-form');
    if (!form) return;

    const btnWhatsApp = document.getElementById('btn-submit-whatsapp');
    const btnEmail = document.getElementById('btn-submit-email');
    const contactPhone = '96879260091';
    const contactEmail = 'info@petlandoman.com';

    function getFormData() {
        const name = document.getElementById('form-name').value.trim();
        const phone = document.getElementById('form-phone').value.trim();
        const email = document.getElementById('form-email').value.trim();
        const subject = document.getElementById('form-subject').value;
        const message = document.getElementById('form-message').value.trim();

        if (!name || !phone || !email || !subject || !message) {
            alert('Please fill out all fields in the contact form.');
            return null;
        }

        return { name, phone, email, subject, message };
    }

    // Submit to WhatsApp
    btnWhatsApp.addEventListener('click', () => {
        const data = getFormData();
        if (!data) return;

        const text = `*New Contact Enquiry - Petland Oman*\n\n` +
                     `*Name:* ${data.name}\n` +
                     `*Phone:* ${data.phone}\n` +
                     `*Email:* ${data.email}\n` +
                     `*Subject:* ${data.subject}\n\n` +
                     `*Message:*\n${data.message}`;

        const url = `https://wa.me/${contactPhone}?text=${encodeURIComponent(text)}`;
        window.open(url, '_blank');
    });

    // Submit to Email
    btnEmail.addEventListener('click', () => {
        const data = getFormData();
        if (!data) return;

        const mailSubject = `[Enquiry] ${data.subject} - ${data.name}`;
        const mailBody = `Name: ${data.name}\n` +
                         `Phone: ${data.phone}\n` +
                         `Email: ${data.email}\n\n` +
                         `Message:\n${data.message}`;

        const url = `mailto:${contactEmail}?subject=${encodeURIComponent(mailSubject)}&body=${encodeURIComponent(mailBody)}`;
        window.location.href = url;
    });
}

/* ==========================================================================
   6. HERO LOGO OVERLAY — fades out as scroll animation frames come in
   ========================================================================== */
function initHeroLogoOverlay() {
    // Integrated directly into CanvasScrollScrubber tick loop for optimized performance
}

/* ==========================================================================
   7. MOBILE CAROUSELS — infinite continuous marquee for services & branches
   ========================================================================== */
function initMobileCarousels() {
    function setupMarquee(trackSelector) {
        const track = document.querySelector(trackSelector);
        if (!track) return;

        // Clone children once to ensure seamless infinite looping translation
        const children = Array.from(track.children);
        children.forEach(child => {
            const clone = child.cloneNode(true);
            track.appendChild(clone);
        });

        // Set up continuous scrolling via scrollLeft ticker
        let scrollSpeed = 0.5; // pixels per frame (adjust for speed)
        let isInteracting = false;
        let interactionTimeout = null;

        let halfway = track.scrollWidth / 2;
        window.addEventListener('resize', () => {
            halfway = track.scrollWidth / 2;
        }, { passive: true });

        function tick() {
            if (!isInteracting) {
                track.scrollLeft += scrollSpeed;

                // Loop halfway: since we cloned once, the total content length is exactly doubled.
                // Reset scrollLeft back to 0 when it passes halfway scrollWidth.
                if (track.scrollLeft >= halfway) {
                    track.scrollLeft -= halfway;
                }
            }
            requestAnimationFrame(tick);
        }

        // Pause auto-scroll on manual touch/drag interaction
        const pauseInteraction = () => {
            isInteracting = true;
            clearTimeout(interactionTimeout);
            interactionTimeout = setTimeout(() => {
                isInteracting = false;
            }, 3000); // Resume auto-scroll after 3 seconds of inactivity
        };

        track.addEventListener('touchstart', pauseInteraction, { passive: true });
        track.addEventListener('touchmove', pauseInteraction, { passive: true });
        
        // Desktop support: pause on hover
        track.addEventListener('mouseenter', () => { isInteracting = true; });
        track.addEventListener('mouseleave', () => { isInteracting = false; });

        track.addEventListener('scroll', () => {
            // Keep index loop matching if user manual scrolls past halfway
            if (track.scrollLeft >= halfway) {
                track.scrollLeft -= halfway;
            } else if (track.scrollLeft <= 0) {
                track.scrollLeft += halfway;
            }
        }, { passive: true });

        // Start scrolling loop
        requestAnimationFrame(tick);
    }

    // Only set up services marquee on mobile viewports
    if (window.innerWidth <= 768) {
        setupMarquee('.service-cards-row');
    }

    // Always set up branches marquee (both desktop and mobile)
    setupMarquee('.branches-grid');
}
