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
    });
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
        this.canvas = document.getElementById(canvasId);
        if (!this.container || !this.canvas) return;

        this.ctx = this.canvas.getContext('2d');
        
        // Detect mobile viewport (768px or below)
        this.isMobile = window.innerWidth <= 768;
        this.frameCount = this.isMobile ? 211 : frameCount; // 211 for mobile, 169 for desktop

        this.images = [];
        this.currentProgress = 0;
        this.targetProgress = 0;
        this.lerpFactor = 0.08; // smooth scrubbing factor
        this.lastRenderedFrame = -1;

        // Overlay UI elements
        this.loadingOverlay = document.getElementById('canvas-loading');

        this.init();
    }

    init() {
        // Set canvas resolution
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas(), { passive: true });

        // Start loading images progressively
        this.preloadImages();

        // Listen for scroll
        window.addEventListener('scroll', () => this.handleScroll(), { passive: true });

        // Start render ticker
        this.tick();
    }

    resizeCanvas() {
        const dpr = window.devicePixelRatio || 1;
        this.canvas.width = window.innerWidth * dpr;
        this.canvas.height = window.innerHeight * dpr;
        
        // Draw the last rendered frame to keep canvas correct after resize
        if (this.lastRenderedFrame !== -1) {
            this.drawFrame(this.lastRenderedFrame);
        }
    }

    preloadImages() {
        let loadedCount = 0;

        // Helper to format frame path
        const getFramePath = (index) => {
            const paddedIndex = String(index).padStart(3, '0');
            const dir = this.isMobile 
                ? 'hero%20section%20scroll%20animation%20frames%20for%20mobile%20view'
                : 'hero%20section%20scroll%20animation%20frames';
            return `${dir}/ezgif-frame-${paddedIndex}.png`;
        };

        // Load an image returning a promise
        const loadImage = (index) => {
            return new Promise((resolve) => {
                const img = new Image();
                img.onload = () => {
                    this.images[index] = img;
                    loadedCount++;
                    resolve(true);
                };
                img.onerror = () => {
                    // Fail gracefully
                    resolve(false);
                };
                img.src = getFramePath(index);
            });
        };

        // PRIORITY 1: Load Frame 1 immediately for first paint
        loadImage(1).then(() => {
            // Render first frame immediately
            this.drawFrame(1);

            // PRIORITY 2: Load the starting sequence (Frames 2-30) for instant scrolling feedback
            const priority2Promises = [];
            for (let i = 2; i <= 30 && i <= this.frameCount; i++) {
                priority2Promises.push(loadImage(i));
            }

            Promise.all(priority2Promises).then(() => {
                // Fade out loader once the initial 30 frames are ready
                if (this.loadingOverlay) {
                    this.loadingOverlay.classList.add('fade-out');
                }

                // PRIORITY 3: Sparse loading of remaining sequence (every 5th frame)
                // This builds a fast framerate placeholder structure across the full scroll area
                const priority3Promises = [];
                for (let i = 35; i <= this.frameCount; i += 5) {
                    if (!this.images[i]) {
                        priority3Promises.push(loadImage(i));
                    }
                }

                Promise.all(priority3Promises).then(() => {
                    // PRIORITY 4: Load all intermediate frames in sequence
                    const remainingIndices = [];
                    for (let i = 2; i <= this.frameCount; i++) {
                        if (!this.images[i]) {
                            remainingIndices.push(i);
                        }
                    }

                    // Load remainder sequentially to not flood network
                    let indexPointer = 0;
                    const loadNextSequential = () => {
                        if (indexPointer >= remainingIndices.length) return;
                        loadImage(remainingIndices[indexPointer]).then(() => {
                            indexPointer++;
                            loadNextSequential();
                        });
                    };

                    // Start parallel loaders
                    const parallelLoadersCount = 4;
                    for (let i = 0; i < parallelLoadersCount; i++) {
                        loadNextSequential();
                    }
                });
            });
        });
    }

    handleScroll() {
        const rect = this.container.getBoundingClientRect();
        const containerHeight = rect.height;
        const viewHeight = window.innerHeight;
        const totalScrollable = containerHeight - viewHeight;
        
        if (totalScrollable <= 0) return;

        const currentScroll = -rect.top;
        let progress = currentScroll / totalScrollable;
        progress = Math.min(Math.max(0, progress), 1);

        this.targetProgress = progress;
    }

    tick() {
        // Smoothly lerp current progress to target progress
        this.currentProgress += (this.targetProgress - this.currentProgress) * this.lerpFactor;
        
        // Calculate frame index
        const frameIndex = Math.min(
            this.frameCount,
            Math.max(1, Math.round(this.currentProgress * (this.frameCount - 1) + 1))
        );

        if (frameIndex !== this.lastRenderedFrame) {
            this.drawFrame(frameIndex);
            this.lastRenderedFrame = frameIndex;
        }

        requestAnimationFrame(() => this.tick());
    }

    drawFrame(index) {
        // Fallback algorithm to find closest loaded frame to prevent black screens/flickering
        let img = this.images[index];
        if (!img) {
            let offset = 1;
            while (offset < this.frameCount) {
                const prev = index - offset;
                const next = index + offset;
                if (prev >= 1 && this.images[prev]) {
                    img = this.images[prev];
                    break;
                }
                if (next <= this.frameCount && this.images[next]) {
                    img = this.images[next];
                    break;
                }
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
            // Mobile: contain without stretching or cropping, using matching #fdfdfd background
            const r = Math.min(w / iw, h / ih);
            const nw = iw * r;
            const nh = ih * r;
            const x = (w - nw) / 2;
            const y = (h - nh) / 2;

            this.ctx.fillStyle = '#fdfdfd';
            this.ctx.fillRect(0, 0, w, h);
            this.ctx.drawImage(img, x, y, nw, nh);
        } else {
            // Desktop: remain exactly as it is (object-fit: cover)
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
   4. CONTACT FORM SUBMISSION ROUTING
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
