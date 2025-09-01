// 3D tilt effect for cards
document.addEventListener("DOMContentLoaded", function () {
  // Initialize tilt effect on cards
  const cards = document.querySelectorAll(
    ".event-card, .action-card, .calendar-day-cell:not(.empty)"
  );

  cards.forEach((card) => {
    card.addEventListener("mousemove", function (e) {
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;

      const centerX = rect.width / 2;
      const centerY = rect.height / 2;

      const angleY = (x - centerX) / 25;
      const angleX = (centerY - y) / 25;

      this.style.transform = `perspective(1000px) rotateX(${angleX}deg) rotateY(${angleY}deg) scale3d(1.02, 1.02, 1.02)`;
    });

    card.addEventListener("mouseleave", function () {
      this.style.transform =
        "perspective(1000px) rotateX(0) rotateY(0) scale3d(1, 1, 1)";
    });
  });

  // Animated background elements
  createAnimatedBackground();

  // Initialize typing animation for hero text
  const heroTitle = document.querySelector(".hero-title");
  if (heroTitle) {
    heroTitle.classList.add("typing-animation");
  }

  // Add pulse animation to important elements
  const importantElements = document.querySelectorAll(
    ".btn-primary, .nav-link"
  );
  importantElements.forEach((el) => {
    el.addEventListener("mouseenter", () => {
      el.classList.add("pulse");
    });

    el.addEventListener("mouseleave", () => {
      el.classList.remove("pulse");
    });
  });
});

// Create animated background elements
function createAnimatedBackground() {
  const bgContainer = document.createElement("div");
  bgContainer.className = "animated-bg";

  for (let i = 0; i < 5; i++) {
    const element = document.createElement("div");
    element.className = "bg-element";

    // Random position and size
    const size = Math.random() * 200 + 50;
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;

    element.style.width = `${size}px`;
    element.style.height = `${size}px`;
    element.style.top = `${posY}%`;
    element.style.left = `${posX}%`;

    // Random color
    const colors = [
      "linear-gradient(135deg, #6366f1, transparent)",
      "linear-gradient(135deg, #f471b5, transparent)",
      "linear-gradient(135deg, #10b981, transparent)",
      "linear-gradient(135deg, #f59e0b, transparent)",
    ];
    element.style.background =
      colors[Math.floor(Math.random() * colors.length)];

    // Random animation
    const duration = Math.random() * 30 + 15;
    const delay = Math.random() * 10;
    element.style.animationDuration = `${duration}s`;
    element.style.animationDelay = `${delay}s`;

    bgContainer.appendChild(element);
  }

  document.body.appendChild(bgContainer);
}

// Parallax effect on scroll
window.addEventListener("scroll", function () {
  const scrolled = window.pageYOffset;
  const parallaxElements = document.querySelectorAll(
    ".floating-calendar, .floating-event"
  );

  parallaxElements.forEach((element, index) => {
    const rate = scrolled * (0.5 + index * 0.1);
    element.style.transform = `translateY(${rate}px) translateZ(${
      index * 10
    }px)`;
  });
});

// Interactive calendar day hover
document.querySelectorAll(".calendar-day-cell:not(.empty)").forEach((day) => {
  day.addEventListener("mouseenter", function () {
    this.style.transform = "translateZ(20px) scale(1.05)";
    this.style.zIndex = "10";
  });

  day.addEventListener("mouseleave", function () {
    this.style.transform = "translateZ(0) scale(1)";
    this.style.zIndex = "1";
  });
});
