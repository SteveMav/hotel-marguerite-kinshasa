(function () {
  const root = document.documentElement;
  const menu = document.getElementById("site-menu");
  const navToggle = document.querySelector(".nav-toggle");
  const themeToggle = document.querySelector(".theme-toggle");
  const storedTheme = localStorage.getItem("hm-theme");

  if (storedTheme === "light" || storedTheme === "dark") {
    root.dataset.theme = storedTheme;
  }

  if (navToggle && menu) {
    navToggle.addEventListener("click", () => {
      const isOpen = menu.classList.toggle("is-open");
      navToggle.setAttribute("aria-expanded", String(isOpen));
    });

    menu.addEventListener("click", (event) => {
      if (event.target instanceof HTMLAnchorElement) {
        menu.classList.remove("is-open");
        navToggle.setAttribute("aria-expanded", "false");
      }
    });
  }

  if (themeToggle) {
    themeToggle.addEventListener("click", () => {
      const current = root.dataset.theme;
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
      const next = current ? (current === "dark" ? "light" : "dark") : (prefersDark ? "light" : "dark");
      root.dataset.theme = next;
      localStorage.setItem("hm-theme", next);
    });
  }

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12 });

    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  const form = document.getElementById("booking-form");
  if (form) {
    const params = new URLSearchParams(window.location.search);
    const roomParam = params.get("room");
    const roomSelect = document.getElementById("room-type");
    const status = document.getElementById("form-status");

    if (roomParam && roomSelect instanceof HTMLSelectElement) {
      const map = {
        classique: "Chambre Classique",
        confort: "Chambre Confort",
        suite: "Suite Familiale"
      };
      roomSelect.value = map[roomParam] || roomSelect.value;
    }

    form.addEventListener("submit", (event) => {
      event.preventDefault();
      const data = new FormData(form);
      const name = String(data.get("guest-name") || "").trim() || "Client";
      const arrival = String(data.get("arrival") || "").trim() || "date à confirmer";
      const nights = String(data.get("nights") || "1").trim();
      const room = String(data.get("room-type") || "À conseiller");
      const guests = String(data.get("guests") || "1").trim();
      const notes = String(data.get("notes") || "").trim();
      const message = [
        "Bonjour Hotel Marguerite,",
        `Je m'appelle ${name}.`,
        `Je souhaite demander une réservation pour ${guests} personne(s), ${nights} nuit(s), arrivée ${arrival}.`,
        `Chambre souhaitée : ${room}.`,
        notes ? `Message : ${notes}` : "Pouvez-vous me confirmer la disponibilité et le tarif ?"
      ].join("\n");

      if (status) {
        status.textContent = "Message prêt, ouverture de WhatsApp.";
      }

      window.open(`https://wa.me/243998386650?text=${encodeURIComponent(message)}`, "_blank", "noopener");
    });
  }
})();

