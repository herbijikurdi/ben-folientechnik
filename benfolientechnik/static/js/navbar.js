const hamburger = document.querySelector(".hamburger");
const navMenu = document.querySelector(".nav-menu");
const servicesToggle = document.getElementById("services-toggle");
const servicesDropdown = document.getElementById("services-dropdown");
const referenceToggle = document.getElementById("reference-toggle");
const referenceDropdown = document.getElementById("reference-dropdown");

hamburger.addEventListener("click", () => {
  hamburger.classList.toggle("active");
  navMenu.classList.toggle("active");
});

servicesToggle.addEventListener("click", (e) => {
  e.preventDefault();
  servicesDropdown.classList.toggle("active");

  referenceDropdown.classList.remove("active");
  referenceToggle.querySelector(".dropdown-arrow").textContent = "▼";

  const arrow = servicesToggle.querySelector(".dropdown-arrow");
  if (servicesDropdown.classList.contains("active")) {
    arrow.textContent = "▲";
  } else {
    arrow.textContent = "▼";
  }
});

referenceToggle.addEventListener("click", (e) => {
  e.preventDefault();
  referenceDropdown.classList.toggle("active");

  servicesDropdown.classList.remove("active");
  servicesToggle.querySelector(".dropdown-arrow").textContent = "▼";

  const arrow = referenceToggle.querySelector(".dropdown-arrow");
  if (referenceDropdown.classList.contains("active")) {
    arrow.textContent = "▲";
  } else {
    arrow.textContent = "▼";
  }
});

document.querySelectorAll(".nav-link:not(#services-toggle):not(#reference-toggle)").forEach((n) =>
  n.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    servicesDropdown.classList.remove("active");
    referenceDropdown.classList.remove("active");
    document.querySelector("#services-toggle .dropdown-arrow").textContent = "▼";
    document.querySelector("#reference-toggle .dropdown-arrow").textContent = "▼";
  })
);

document.querySelectorAll(".dropdown-item").forEach((item) =>
  item.addEventListener("click", () => {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    servicesDropdown.classList.remove("active");
    referenceDropdown.classList.remove("active");
    document.querySelector("#services-toggle .dropdown-arrow").textContent = "▼";
    document.querySelector("#reference-toggle .dropdown-arrow").textContent = "▼";
  })
);

document.addEventListener("click", (e) => {
  if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
    hamburger.classList.remove("active");
    navMenu.classList.remove("active");
    servicesDropdown.classList.remove("active");
    referenceDropdown.classList.remove("active");
    document.querySelector("#services-toggle .dropdown-arrow").textContent = "▼";
    document.querySelector("#reference-toggle .dropdown-arrow").textContent = "▼";
  }
});
