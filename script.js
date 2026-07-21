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

    let isScrolled = false;

    window.addEventListener('scroll', () => {
        const scrolled = window.scrollY > 50;
        if (scrolled !== isScrolled) {
            isScrolled = scrolled;
            if (isScrolled) {
                header.classList.add('scrolled');
            } else {
                header.classList.remove('scrolled');
            }
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

        // Detect mobile viewport (768px or below)
        this.isMobile  = window.innerWidth <= 768;
        this.frameCount = this.isMobile ? 211 : frameCount; // 211 mobile / 169 desktop

        this.images = [];

        // --- Scroll state ---
        // Desktop uses smooth lerp; mobile maps scroll directly to avoid lag
        this.currentProgress = 0;
        this.targetProgress  = 0;
        this.lerpFactor      = this.isMobile ? 1 : 0.08; // 1 = no easing on mobile

        this.lastRenderedFrame = -1;
        this.isMoving = false; // prevents duplicate rAF loops, tracks active rendering

        this.containerOffsetTop = 0;
        this.containerHeight = 0;

        this.init();
    }

    init() {
        this.updateMetrics();
        this.resizeCanvas();
        window.addEventListener('resize', () => {
            this.updateMetrics();
            this.resizeCanvas();
        }, { passive: true });

        // Apply GPU acceleration hint to canvas on mobile
        if (this.isMobile) {
            this.canvas.style.willChange   = 'transform';
            this.canvas.style.transform    = 'translateZ(0)';
            this.canvas.style.backfaceVisibility = 'hidden';
        }

        this.preloadImages();

        window.addEventListener('scroll', () => {
            this.handleScroll();
        }, { passive: true });
    }

    updateMetrics() {
        const rect = this.container.getBoundingClientRect();
        this.containerOffsetTop = rect.top + window.scrollY;
        this.containerHeight = rect.height;
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

    preloadImages() {
        const getFramePath = (index) => {
            const pad = String(index).padStart(3, '0');
            const pathPrefix = window.location.pathname.includes('/pages/') ? '../' : '';
            const dir = this.isMobile
                ? 'assets/frames/hero_mobile'
                : 'assets/frames/hero_desktop';
            return `${pathPrefix}${dir}/ezgif-frame-${pad}.png`;
        };

        const loadImage = (index) => new Promise((resolve) => {
            if (this.images[index]) { resolve(true); return; }
            const img  = new Image();
            img.onload = () => { this.images[index] = img; resolve(true); };
            img.onerror = () => resolve(false);
            img.src = getFramePath(index);
        });

        // PRIORITY 1: Frame 1 → immediate first paint
        loadImage(1).then(() => {
            this.drawFrame(1);
            this.lastRenderedFrame = 1;

            // PRIORITY 2: Frames 2-20 → fast early-scroll coverage
            const p2 = [];
            for (let i = 2; i <= Math.min(20, this.frameCount); i++) p2.push(loadImage(i));

            Promise.all(p2).then(() => {
                // PRIORITY 3: Sparse every-4th frame across the full sequence
                const p3 = [];
                for (let i = 24; i <= this.frameCount; i += 4) {
                    if (!this.images[i]) p3.push(loadImage(i));
                }

                Promise.all(p3).then(() => {
                    // PRIORITY 4: Fill all remaining frames
                    const remaining = [];
                    for (let i = 2; i <= this.frameCount; i++) {
                        if (!this.images[i]) remaining.push(i);
                    }

                    // More parallel loaders on mobile to saturate bandwidth faster
                    const loaderCount = this.isMobile ? 6 : 4;
                    let ptr = 0;
                    const next = () => {
                        if (ptr >= remaining.length) return;
                        loadImage(remaining[ptr++]).then(next);
                    };
                    for (let i = 0; i < loaderCount; i++) next();
                });
            });
        });
    }

    handleScroll() {
        const totalScrollable = this.containerHeight - window.innerHeight;
        if (totalScrollable <= 0) return;

        const scrolled = window.scrollY - this.containerOffsetTop;
        let progress   = scrolled / totalScrollable;
        progress       = Math.min(Math.max(0, progress), 1);

        this.targetProgress = progress;

        // Start requestAnimationFrame loop if not active
        if (!this.isMoving) {
            this.isMoving = true;
            requestAnimationFrame(() => this.tick());
        }
    }

    tick() {
        if (!this.isMoving) return;

        // Lerp (desktop) or direct (mobile)
        if (this.lerpFactor < 1) {
            this.currentProgress += (this.targetProgress - this.currentProgress) * this.lerpFactor;
        } else {
            this.currentProgress = this.targetProgress;
        }

        const frameIndex = Math.min(
            this.frameCount,
            Math.max(1, Math.round(this.currentProgress * (this.frameCount - 1) + 1))
        );

        // Skip draw if frame hasn't changed — eliminates unnecessary GPU work
        if (frameIndex !== this.lastRenderedFrame) {
            this.drawFrame(frameIndex);
            this.lastRenderedFrame = frameIndex;
        }

        // Desktop: stop loop once animation has settled
        if (!this.isMobile) {
            const diff = Math.abs(this.targetProgress - this.currentProgress);
            if (diff < 0.0001) {
                this.currentProgress = this.targetProgress;
                this.isMoving = false;
                // Final render to snap exactly to target
                const finalFrame = Math.min(
                    this.frameCount,
                    Math.max(1, Math.round(this.currentProgress * (this.frameCount - 1) + 1))
                );
                if (finalFrame !== this.lastRenderedFrame) {
                    this.drawFrame(finalFrame);
                    this.lastRenderedFrame = finalFrame;
                }
                return;
            }
        } else {
            // Mobile: direct mapped progress is completed instantly in one frame
            this.isMoving = false;
            return;
        }

        requestAnimationFrame(() => this.tick());
    }

    drawFrame(index) {
        // Fallback: find nearest loaded frame to prevent blank screens
        let img = this.images[index];
        if (!img) {
            let offset = 1;
            while (offset < this.frameCount) {
                const prev = index - offset;
                const next = index + offset;
                if (prev >= 1 && this.images[prev]) { img = this.images[prev]; break; }
                if (next <= this.frameCount && this.images[next]) { img = this.images[next]; break; }
                offset++;
            }
        }
        if (!img) return;

        const w = this.canvas.width;
        const h = this.canvas.height;

        this.ctx.clearRect(0, 0, w, h);

        const iw = img.width;
        const ih = img.height;

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
            // Desktop: object-fit cover — UNCHANGED
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
};

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
    const overlay   = document.getElementById('hero-logo-overlay');
    const container = document.getElementById('scroll-canvas-section');
    if (!overlay || !container) return;

    // Fade the logo out over the first 30% of the scroll-canvas travel
    const FADE_END = 0.30;

    let containerOffsetTop = 0;
    let containerHeight = 0;

    const updateMetrics = () => {
        const rect = container.getBoundingClientRect();
        containerOffsetTop = rect.top + window.scrollY;
        containerHeight = rect.height;
    };

    updateMetrics();
    window.addEventListener('resize', updateMetrics, { passive: true });

    const update = () => {
        const totalScrollable = containerHeight - window.innerHeight;
        if (totalScrollable <= 0) return;

        const scrolled  = window.scrollY - containerOffsetTop;
        const progress  = Math.min(Math.max(0, scrolled / totalScrollable), 1);

        // Map 0 → FADE_END to opacity 1 → 0
        const opacity = Math.max(0, 1 - (progress / FADE_END));
        overlay.style.opacity = opacity;
    };

    window.addEventListener('scroll', update, { passive: true });
    update(); // run once on load
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
