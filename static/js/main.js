/**
 * EduPredict - Core Frontend JavaScript
 * Implements:
 * - 3-second animated splash screen on initial visit (sessionStorage)
 * - Dark mode theme switcher with persistence (localStorage)
 * - Toast / flash message auto-dismissal
 * - Smooth scroll & modal triggers
 */

document.addEventListener("DOMContentLoaded", function () {
    // 1. Animated Splash Screen Controller (Automatically displays for 3 seconds on open)
    const splash = document.getElementById("splash-screen");
    if (splash) {
        setTimeout(function () {
            splash.classList.add("splash-hidden");
            setTimeout(function () {
                splash.style.display = "none";
            }, 600);
        }, 3000);
    }

    // 2. Dark Mode Toggle
    const themeToggleBtn = document.getElementById("theme-toggle");
    const currentTheme = localStorage.getItem("edupredict_theme");

    if (currentTheme === "dark") {
        document.body.classList.add("dark-mode");
        if (themeToggleBtn) themeToggleBtn.innerHTML = "☀️";
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", function () {
            document.body.classList.toggle("dark-mode");
            const isDark = document.body.classList.contains("dark-mode");
            localStorage.setItem("edupredict_theme", isDark ? "dark" : "light");
            themeToggleBtn.innerHTML = isDark ? "☀️" : "🌙";
        });
    }

    // 3. Auto-dismiss flash alerts after 5 seconds
    const alerts = document.querySelectorAll(".alert");
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = "opacity 0.5s ease, transform 0.5s ease";
            alert.style.opacity = "0";
            alert.style.transform = "translateY(-8px)";
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 5000);
    });
});

// Modal Helpers
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.add("open");
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.classList.remove("open");
}

window.addEventListener("click", function (event) {
    if (event.target.classList.contains("modal-backdrop")) {
        event.target.classList.remove("open");
    }
});
