/**
 * Petland Oman - Core JavaScript Controller
 * Implements: Sticky Header, Mobile Navigation, Smooth Video Scroll-Seeking,
 * Infinite Marquee Speeds, Popups, and Contact Form routing.
 */

document.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initMobileNav();
    initVideoScrollSeek();
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
   2. SMOOTH VIDEO SCROLL-SEEKING
   ========================================================================== */
class VideoScrollSeeker {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        if (!this.container) return;

        this.videoDesktop = document.getElementById('scroll-video-desktop');
        this.videoMobile  = document.getElementById('scroll-video-mobile');
        this.slides       = this.container.querySelectorAll('.overlay-slide');

        this.activeVideo  = null;
        this.targetTime   = 0;
        this.currentTime  = 0;
        this.lerpFactor   = 0.12; // slightly snappier on desktop
        this.isMobile     = false;
        this.mobileMode   = false; // true = autoplay loop, no seek

        this.init();
    }

    init() {
        this.handleResize();
        window.addEventListener('resize', () => this.handleResize(), { passive: true });

        if (!this.mobileMode) {
            // Desktop: allocate scroll space and start seek loop
            const numSlides = this.slides.length || 3;
            this.container.style.height = `${(numSlides + 1) * 100}vh`;
            window.addEventListener('scroll', () => this.handleScroll(), { passive: true });
            this.tick();
        }
        // Mobile: container stays at 100vh (set by CSS), video just autoplays
    }

    handleResize() {
        const width = window.innerWidth;
        const previouslyMobile = this.isMobile;
        this.isMobile  = width <= 768;
        this.mobileMode = this.isMobile;

        if (this.isMobile && this.videoMobile) {
            if (this.videoDesktop) this.videoDesktop.style.display = 'none';
            this.videoMobile.style.display = 'block';
            this.activeVideo = this.videoMobile;
        } else if (this.videoDesktop) {
            if (this.videoMobile) this.videoMobile.style.display = 'none';
            this.videoDesktop.style.display = 'block';
            this.activeVideo = this.videoDesktop;
        }

        if (this.mobileMode && this.activeVideo) {
            // On mobile: ensure the video just autoplays as a loop, no seeking
            this.activeVideo.loop = true;
            this.activeVideo.play().catch(() => {});
            // Collapse container so there's no dead scroll zone
            this.container.style.height = '100vh';
        } else if (!this.mobileMode && this.container) {
            // On desktop: restore scroll-seek container height
            const numSlides = this.slides.length || 3;
            this.container.style.height = `${(numSlides + 1) * 100}vh`;
            // Show first slide
            if (this.slides[0]) this.slides[0].classList.add('active');
        }

        // Reload video if switching breakpoint
        if (this.activeVideo && previouslyMobile !== this.isMobile) {
            if (!this.mobileMode) {
                // Desktop: pause for seek
                this.activeVideo.load();
                this.activeVideo.play().then(() => {
                    this.activeVideo.pause();
                }).catch(() => {});
            }
        }
    }

    handleScroll() {
        // Never seek on mobile — let the video loop
        if (this.mobileMode) return;
        if (!this.activeVideo || isNaN(this.activeVideo.duration)) return;

        const rect            = this.container.getBoundingClientRect();
        const containerHeight = rect.height;
        const viewHeight      = window.innerHeight;
        const totalScrollable = containerHeight - viewHeight;
        const currentScroll   = -rect.top;

        let progress = currentScroll / totalScrollable;
        progress = Math.min(Math.max(0, progress), 1);

        this.targetTime = progress * this.activeVideo.duration;

        // Update slide visibility
        const numSlides = this.slides.length;
        if (numSlides > 0) {
            const unit = 1 / numSlides;
            this.slides.forEach((slide, idx) => {
                const start  = idx * unit;
                const end    = (idx + 1) * unit;
                const margin = 0.05;
                if (progress >= (start - (idx === 0 ? 0 : margin)) && progress <= end) {
                    slide.classList.add('active');
                } else {
                    slide.classList.remove('active');
                }
            });
        }
    }

    tick() {
        // Only runs on desktop (mobileMode skips seek entirely)
        if (!this.mobileMode && this.activeVideo && !isNaN(this.activeVideo.duration)) {
            this.currentTime += (this.targetTime - this.currentTime) * this.lerpFactor;
            const delta = Math.abs(this.targetTime - this.currentTime);
            if (delta > 0.004) {
                this.activeVideo.currentTime = Math.min(
                    Math.max(0, this.currentTime),
                    this.activeVideo.duration - 0.05
                );
            }
        }
        requestAnimationFrame(() => this.tick());
    }
}

function initVideoScrollSeek() {
    const seeker = new VideoScrollSeeker('scroll-section');
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
    const phoneNo = '96890000000';

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
    const contactPhone = '96890000000';
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
