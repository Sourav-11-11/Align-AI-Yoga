/**
 * main.js — Align AI Yoga frontend utilities
 *
 * Keeps only the interactions the app actually uses:
 *   - Flash message auto-dismiss
 *   - Image upload preview
 *   - Smooth scroll-to-top button
 *   - Dashboard modal image viewer
 */

"use strict";

document.addEventListener("DOMContentLoaded", function () {

    /* ── Flash messages ────────────────────────────────────────────────────
       Auto-dismiss Bootstrap alerts after 4 seconds.                       */
    document.querySelectorAll(".alert-dismissible").forEach(function (alert) {
        setTimeout(function () {
            var bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 4000);
    });

    /* ── Image upload preview ──────────────────────────────────────────────
       Shows a thumbnail of the selected file before the form is submitted. */
    var fileInput = document.getElementById("img");
    var preview   = document.getElementById("img-preview");
    if (fileInput && preview) {
        fileInput.addEventListener("change", function () {
            var file = this.files[0];
            if (file) {
                var reader = new FileReader();
                reader.onload = function (e) {
                    preview.src = e.target.result;
                    preview.style.display = "block";
                };
                reader.readAsDataURL(file);
            }
        });
    }

    /* ── Scroll-to-top button ──────────────────────────────────────────────
       Shows the button once the user scrolls past 200 px.                  */
    var topBtn = document.getElementById("back-to-top");
    if (topBtn) {
        window.addEventListener("scroll", function () {
            topBtn.style.display = window.scrollY > 200 ? "block" : "none";
        });
        topBtn.addEventListener("click", function () {
            window.scrollTo({ top: 0, behavior: "smooth" });
        });
    }

    /* ── Dashboard modal image viewer ──────────────────────────────────────
       Clicking a session image opens it full-size in a Bootstrap modal.    */
    var imageModal = document.getElementById("imageModal");
    if (imageModal) {
        imageModal.addEventListener("show.bs.modal", function (event) {
            var trigger  = event.relatedTarget;
            var imgSrc   = trigger ? trigger.getAttribute("data-img-src") : null;
            var modalImg = document.getElementById("modalImage");
            if (modalImg && imgSrc) {
                modalImg.src = imgSrc;
            }
        });
    }

});
