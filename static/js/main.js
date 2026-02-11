(function () {
    const selectEl = document.getElementById("training-select");
    const dateInput = document.getElementById("training-date");
    const messageEl = document.getElementById("form-message");

    const weekdayIndex = {
        sunday: 0,
        monday: 1,
        tuesday: 2,
        wednesday: 3,
        thursday: 4,
        friday: 5,
        saturday: 6,
    };

    function formatDate(date) {
        const yyyy = date.getFullYear();
        const mm = String(date.getMonth() + 1).padStart(2, "0");
        const dd = String(date.getDate()).padStart(2, "0");
        return `${yyyy}-${mm}-${dd}`;
    }

    function nextDateForWeekday(weekday) {
        const target = weekdayIndex[weekday];
        if (target === undefined) return null;
        const today = new Date();
        const current = today.getDay();
        let diff = (target - current + 7) % 7;
        const result = new Date(today);
        result.setDate(today.getDate() + diff);
        return result;
    }

    function updateDateFromTraining() {
        if (!selectEl || !dateInput) return;
        const selected = selectEl.options[selectEl.selectedIndex];
        if (!selected || !selected.dataset.weekday) return;
        const nextDate = nextDateForWeekday(selected.dataset.weekday);
        if (nextDate) {
            dateInput.value = formatDate(nextDate);
        }
    }

    function setMinDate() {
        if (!dateInput) return;
        const today = new Date();
        dateInput.min = formatDate(today);
    }

    function setupSignupButtons() {
        const buttons = document.querySelectorAll(".signup-btn");
        buttons.forEach((btn) => {
            btn.addEventListener("click", () => {
                const trainingId = btn.getAttribute("data-training-id");
                if (selectEl && trainingId) {
                    selectEl.value = trainingId;
                    updateDateFromTraining();
                }
                const signupSection = document.getElementById("signup");
                if (signupSection) {
                    signupSection.scrollIntoView({ behavior: "smooth" });
                }
            });
        });
    }

    function setupCarousels() {
        const carousels = document.querySelectorAll(".carousel");
        carousels.forEach((carousel) => {
            const track = carousel.querySelector(".carousel-track");
            const prev = carousel.querySelector(".carousel-control.prev");
            const next = carousel.querySelector(".carousel-control.next");
            if (!track || !prev || !next) return;

            const getScrollAmount = () => {
                const firstItem = track.children[0];
                if (!firstItem) return 300;
                const gap = parseFloat(getComputedStyle(track).columnGap || "24");
                return firstItem.getBoundingClientRect().width + gap;
            };

            prev.addEventListener("click", () => {
                track.scrollBy({ left: -getScrollAmount(), behavior: "smooth" });
            });

            next.addEventListener("click", () => {
                track.scrollBy({ left: getScrollAmount(), behavior: "smooth" });
            });

            track.addEventListener("keydown", (event) => {
                if (event.key === "ArrowLeft") {
                    track.scrollBy({ left: -getScrollAmount(), behavior: "smooth" });
                }
                if (event.key === "ArrowRight") {
                    track.scrollBy({ left: getScrollAmount(), behavior: "smooth" });
                }
            });
        });
    }

    function setupSmoothScroll() {
        document.querySelectorAll('a[href^=\"#\"], a[href^=\"/#\"]').forEach((anchor) => {
            anchor.addEventListener("click", (event) => {
                const href = anchor.getAttribute("href");
                if (!href) return;
                if (href.startsWith("/#") && window.location.pathname !== "/") {
                    return;
                }
                const targetId = href.startsWith("/#") ? href.substring(1) : href;
                if (!targetId || targetId === "#") return;
                const target = document.querySelector(targetId);
                if (target) {
                    event.preventDefault();
                    target.scrollIntoView({ behavior: "smooth" });
                }
            });
        });
    }

    function setupForm() {
        const form = document.getElementById("signup-form");
        if (!form) return;

        form.addEventListener("submit", async (event) => {
            event.preventDefault();
            messageEl.textContent = "";
            const formData = new FormData(form);
            const csrfToken = form.querySelector("input[name=csrfmiddlewaretoken]").value;

            try {
                const response = await fetch(form.action, {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken,
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    body: formData,
                });

                const payload = await response.json();
                if (response.ok && payload.success) {
                    messageEl.textContent = payload.message;
                    form.reset();
                    setMinDate();
                } else {
                    const firstError = payload.errors && Object.values(payload.errors)[0];
                    messageEl.textContent = firstError ? firstError[0] : "Помилка. Спробуйте ще раз.";
                }
            } catch (error) {
                messageEl.textContent = "Помилка зʼєднання. Спробуйте ще раз.";
            }
        });
    }

    function setupStravaLinks() {
        const links = document.querySelectorAll(".strava-open-link");
        if (!links.length) return;

        const isMobile = /Android|iPhone|iPad|iPod/i.test(navigator.userAgent || "");
        if (!isMobile) return;

        links.forEach((link) => {
            link.removeAttribute("target");
            link.addEventListener("click", (event) => {
                const appUrl = link.dataset.appUrl;
                const webUrl = link.dataset.webUrl || link.href;
                if (!appUrl || !webUrl) return;

                event.preventDefault();
                let appOpened = false;
                const onVisibilityChange = () => {
                    if (document.hidden) {
                        appOpened = true;
                    }
                };

                document.addEventListener("visibilitychange", onVisibilityChange);
                window.location.href = appUrl;

                setTimeout(() => {
                    document.removeEventListener("visibilitychange", onVisibilityChange);
                    if (!appOpened) {
                        window.location.href = webUrl;
                    }
                }, 900);
            });
        });
    }

    if (selectEl) {
        selectEl.addEventListener("change", updateDateFromTraining);
    }

    setMinDate();
    setupSignupButtons();
    setupCarousels();
    setupSmoothScroll();
    setupForm();
    setupStravaLinks();
})();
