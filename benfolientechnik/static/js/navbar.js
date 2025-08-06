const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const servicesToggle = document.getElementById("services-toggle");
const servicesDropdown = document.getElementById("services-dropdown");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
});

servicesToggle.addEventListener("click", (e) => {
  e.preventDefault();
  servicesDropdown.classList.toggle("active");

  const arrow = servicesToggle.querySelector(".dropdown-arrow");
  if (servicesDropdown.classList.contains("active")) {
    arrow.textContent = "▲";
  } else {
    arrow.textContent = "▼";
  }
});

document.querySelectorAll(".nav-link:not(#services-toggle)").forEach((n) =>
  n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    servicesDropdown.classList.remove("active");
    document.querySelector(".dropdown-arrow").textContent = "▼";
  })
);

document.querySelectorAll(".dropdown-item").forEach((item) =>
  item.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    servicesDropdown.classList.remove("active");
    document.querySelector(".dropdown-arrow").textContent = "▼";
  })
);

document.addEventListener("click", (e) => {
  if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    servicesDropdown.classList.remove("active");
    document.querySelector(".dropdown-arrow").textContent = "▼";
  }
});
