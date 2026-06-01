// ═══════════════════ Pagination Dots ═══════════════════
const slides = document.querySelectorAll('.slide');
const pagination = document.getElementById('pagination');

slides.forEach((_, i) => {
    const dot = document.createElement('button');
    dot.className = 'pag-dot';
    dot.setAttribute('aria-label', `Go to slide ${i + 1}`);
    dot.addEventListener('click', () => {
        slides[i].scrollIntoView({ behavior: 'smooth' });
    });
    pagination.appendChild(dot);
});

const pagDots = document.querySelectorAll('.pag-dot');

// ═══════════════════ Intersection Observer for Animations ═══════════════════
const observerOptions = { threshold: 0.2 };
let currentSlide = 0;

const slideObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            // Update pagination
            const idx = Array.from(slides).indexOf(entry.target);
            currentSlide = idx;
            pagDots.forEach((dot, i) => {
                dot.classList.toggle('active', i === idx);
            });

            // Animate items in this slide
            const items = entry.target.querySelectorAll('.animate-item');
            items.forEach(item => item.classList.add('visible'));
        }
    });
}, observerOptions);

slides.forEach(slide => slideObserver.observe(slide));

// ═══════════════════ Keyboard Navigation ═══════════════════
document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        if (currentSlide < slides.length - 1) {
            slides[currentSlide + 1].scrollIntoView({ behavior: 'smooth' });
        }
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        if (currentSlide > 0) {
            slides[currentSlide - 1].scrollIntoView({ behavior: 'smooth' });
        }
    } else if (e.key === 'Home') {
        e.preventDefault();
        slides[0].scrollIntoView({ behavior: 'smooth' });
    } else if (e.key === 'End') {
        e.preventDefault();
        slides[slides.length - 1].scrollIntoView({ behavior: 'smooth' });
    }
});

// ═══════════════════ Initial State ═══════════════════
// Activate first slide animations on load
window.addEventListener('load', () => {
    pagDots[0]?.classList.add('active');
    const firstItems = slides[0]?.querySelectorAll('.animate-item');
    if (firstItems) {
        firstItems.forEach(item => item.classList.add('visible'));
    }
});
