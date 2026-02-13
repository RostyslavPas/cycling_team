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

    function setupMobileMenu() {
        const toggle = document.querySelector("[data-menu-toggle]");
        const menu = document.getElementById("mobile-menu");
        if (!toggle || !menu) return;

        const links = menu.querySelectorAll(".mobile-nav-link");

        const openMenu = () => {
            document.body.classList.add("menu-open");
            toggle.setAttribute("aria-expanded", "true");
            menu.setAttribute("aria-hidden", "false");
        };

        const closeMenu = () => {
            document.body.classList.remove("menu-open");
            toggle.setAttribute("aria-expanded", "false");
            menu.setAttribute("aria-hidden", "true");
        };

        toggle.addEventListener("click", () => {
            if (document.body.classList.contains("menu-open")) closeMenu();
            else openMenu();
        });

        links.forEach((link) => {
            link.addEventListener("click", () => {
                closeMenu();
            });
        });

        document.addEventListener("keydown", (event) => {
            if (event.key === "Escape") {
                closeMenu();
            }
        });

        window.addEventListener("resize", () => {
            if (window.innerWidth > 860) {
                closeMenu();
            }
        });
    }

    function setupHeroCarousel() {
        const root = document.querySelector("[data-hero-carousel]");
        if (!root) return;

        const slides = Array.from(root.querySelectorAll(".hero-media-slide"));
        const prevBtn = root.querySelector(".hero-media-control.prev");
        const nextBtn = root.querySelector(".hero-media-control.next");
        const dotsContainer = root.querySelector(".hero-media-dots");
        if (slides.length <= 1 || !prevBtn || !nextBtn || !dotsContainer) return;

        let currentIndex = slides.findIndex((slide) => slide.classList.contains("is-active"));
        if (currentIndex < 0) currentIndex = 0;

        const dots = slides.map((_, index) => {
            const dot = document.createElement("button");
            dot.type = "button";
            dot.className = "hero-media-dot";
            dot.setAttribute("aria-label", `Показати фото ${index + 1}`);
            dot.addEventListener("click", () => {
                goTo(index);
            });
            dotsContainer.appendChild(dot);
            return dot;
        });

        const render = () => {
            slides.forEach((slide, index) => {
                slide.classList.toggle("is-active", index === currentIndex);
            });
            dots.forEach((dot, index) => {
                dot.classList.toggle("is-active", index === currentIndex);
            });
        };

        const goTo = (index) => {
            const total = slides.length;
            currentIndex = (index + total) % total;
            render();
        };

        prevBtn.addEventListener("click", () => goTo(currentIndex - 1));
        nextBtn.addEventListener("click", () => goTo(currentIndex + 1));

        let touchStartX = 0;
        let touchEndX = 0;
        root.addEventListener(
            "touchstart",
            (event) => {
                touchStartX = event.changedTouches[0].clientX;
            },
            { passive: true }
        );
        root.addEventListener(
            "touchend",
            (event) => {
                touchEndX = event.changedTouches[0].clientX;
                const deltaX = touchEndX - touchStartX;
                if (Math.abs(deltaX) < 40) return;
                if (deltaX < 0) goTo(currentIndex + 1);
                if (deltaX > 0) goTo(currentIndex - 1);
            },
            { passive: true }
        );

        let autoplayId = null;
        const stopAutoplay = () => {
            if (autoplayId) {
                window.clearInterval(autoplayId);
                autoplayId = null;
            }
        };
        const startAutoplay = () => {
            stopAutoplay();
            autoplayId = window.setInterval(() => {
                goTo(currentIndex + 1);
            }, 4500);
        };

        root.addEventListener("mouseenter", stopAutoplay);
        root.addEventListener("mouseleave", startAutoplay);
        document.addEventListener("visibilitychange", () => {
            if (document.hidden) stopAutoplay();
            else startAutoplay();
        });

        render();
        startAutoplay();
    }

    function setupBackgroundVideos() {
        const videos = document.querySelectorAll(".hero-video-bg video, .academy-video-bg video");
        if (!videos.length) return;

        videos.forEach((video) => {
            const markReady = () => {
                video.classList.add("is-ready");
            };

            if (video.readyState >= 2) {
                markReady();
            } else {
                video.addEventListener("loadeddata", markReady, { once: true });
                video.addEventListener("canplay", markReady, { once: true });
            }
        });
    }

    function setupCarousels() {
        const carousels = document.querySelectorAll(".carousel");
        carousels.forEach((carousel) => {
            const track = carousel.querySelector(".carousel-track");
            const prev = carousel.querySelector(".carousel-control.prev");
            const next = carousel.querySelector(".carousel-control.next");
            const carouselType = carousel.dataset.carousel;
            const dotsContainer = carouselType
                ? document.querySelector(`[data-carousel-dots="${carouselType}"]`)
                : null;
            if (!track || !prev || !next) return;

            const slides = Array.from(track.children);
            const dots = [];

            const getScrollAmount = () => {
                const firstItem = track.children[0];
                if (!firstItem) return 300;
                const gap = parseFloat(getComputedStyle(track).columnGap || "24");
                return firstItem.getBoundingClientRect().width + gap;
            };

            const getActiveSlideIndex = () => {
                const amount = getScrollAmount();
                if (!amount) return 0;
                const index = Math.round(track.scrollLeft / amount);
                return Math.max(0, Math.min(index, slides.length - 1));
            };

            const setActiveDot = (activeIndex) => {
                dots.forEach((dot, index) => {
                    dot.classList.toggle("is-active", index === activeIndex);
                });
            };

            if (dotsContainer) {
                dotsContainer.innerHTML = "";
                if (slides.length > 1) {
                    slides.forEach((_, index) => {
                        const dot = document.createElement("button");
                        dot.type = "button";
                        dot.className = "carousel-dot";
                        dot.setAttribute("aria-label", `Перейти до слайду ${index + 1}`);
                        dot.addEventListener("click", () => {
                            track.scrollTo({
                                left: getScrollAmount() * index,
                                behavior: "smooth",
                            });
                        });
                        dotsContainer.appendChild(dot);
                        dots.push(dot);
                    });
                    setActiveDot(0);
                }
            }

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

            if (dots.length) {
                let rafId = null;
                track.addEventListener(
                    "scroll",
                    () => {
                        if (rafId) return;
                        rafId = window.requestAnimationFrame(() => {
                            setActiveDot(getActiveSlideIndex());
                            rafId = null;
                        });
                    },
                    { passive: true }
                );

                window.addEventListener("resize", () => {
                    setActiveDot(getActiveSlideIndex());
                });
            }
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

        const blurActiveElement = () => {
            const active = document.activeElement;
            if (active && typeof active.blur === "function") {
                active.blur();
            }
        };

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
                    blurActiveElement();
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
    setupMobileMenu();
    setupSignupButtons();
    setupHeroCarousel();
    setupBackgroundVideos();
    setupCarousels();
    setupSmoothScroll();
    setupForm();
    setupStravaLinks();
})();
