tailwind.config = {
    theme: {
        extend: {
            colors: {
                primary: '#EF4444',
                'primary-dark': '#1E293B',
                accent: '#F59E0B',
                muted: '#64748B'
            },
            fontFamily: {
                'sans': ['Inter', 'system-ui', 'sans-serif']
            }
        }
    }
}
document.querySelectorAll("#loginModal form, #registerModal form").forEach(form => {
    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        const formData = new FormData(form);

        try {
            const response = await fetch(form.action, {
                method: "POST",
                body: formData,
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });

            const data = await response.json();
            const errorBox = form.querySelector(".error-message");

            if (data.success) {
                // закрываем модалку
                if (form.closest("#loginModal")) closeModal(document.getElementById("loginModal"));
                if (form.closest("#registerModal")) closeModal(document.getElementById("registerModal"));
                window.location.reload(); // обновляем шапку, корзину и т.д.
            } else {
                if (errorBox) {
                    errorBox.textContent = data.error;
                    errorBox.classList.remove("hidden");
                } else {
                    alert(data.error);
                }
            }
        } catch (err) {
            console.error("Ошибка запроса:", err);
        }
    });
});


const initPhoneValidation = () => {
    const phoneInputs = document.querySelectorAll('input[type="tel"], input[id*="phone"], input[id*="Phone"]');

    phoneInputs.forEach(input => {
        if (!input.value) input.value = '+998';

        input.addEventListener('input', (e) => {
            let value = e.target.value;

            if (!value.startsWith('+998')) {
                value = '+998';
            }

            if (value.length > 12) {
                value = value.slice(0, 12);
            }

            e.target.value = value;
        });

        input.addEventListener('focus', (e) => {
            if (!e.target.value) {
                e.target.value = '+998';
            }
        });
    });
};

document.addEventListener('DOMContentLoaded', () => {
    initPhoneValidation();

    const mobileMenu = document.getElementById('mobile-menu');
    const loginModal = document.getElementById('loginModal');
    const loginModalContent = document.getElementById('loginModalContent');
    const openLoginModalBtn = document.getElementById('openLoginModal');
    const closeLoginModalBtn = document.getElementById('closeLoginModal');
    const loginPasswordField = document.getElementById('loginPasswordField');
    const toggleLoginPasswordBtn = document.getElementById('toggleLoginPassword');
    const loginEyeOpen = document.getElementById('loginEyeOpen');
    const loginEyeClosed = document.getElementById('loginEyeClosed');
    const registerModal = document.getElementById('registerModal');
    const registerModalContent = document.getElementById('registerModalContent');
    const openRegisterModalBtn = document.getElementById('openRegisterModal');
    const closeRegisterModalBtn = document.getElementById('closeRegisterModal');
    const registerPasswordField = document.getElementById('registerPasswordField');
    const toggleRegisterPasswordBtn = document.getElementById('toggleRegisterPassword');
    const registerEyeOpen = document.getElementById('registerEyeOpen');
    const registerEyeClosed = document.getElementById('registerEyeClosed');
    const openLoginModalFromRegisterBtn = document.getElementById('openLoginModalFromRegister');

    if (mobileMenu) {
        mobileMenu.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : 'auto';
        });
    }

    const openModal = (modal) => {
        if (loginModal) loginModal.classList.add('hidden');
        if (registerModal) registerModal.classList.add('hidden');
        if (modal) {
            modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
        }
    };

    const closeModal = (modal) => {
        if (modal) {
            modal.classList.add('hidden');
            document.body.style.overflow = 'auto';
        }
    };

    if (openLoginModalBtn && loginModal) {
        openLoginModalBtn.addEventListener('click', () => openModal(loginModal));
    }

    if (closeLoginModalBtn && loginModal) {
        closeLoginModalBtn.addEventListener('click', () => closeModal(loginModal));
    }

    if (openRegisterModalBtn && registerModal) {
        openRegisterModalBtn.addEventListener('click', () => openModal(registerModal));
    }

    if (closeRegisterModalBtn && registerModal) {
        closeRegisterModalBtn.addEventListener('click', () => closeModal(registerModal));
    }

    if (openLoginModalFromRegisterBtn && loginModal) {
        openLoginModalFromRegisterBtn.addEventListener('click', () => openModal(loginModal));
    }

    if (loginModal && loginModalContent) {
        loginModal.addEventListener('click', (e) => {
            if (e.target === loginModal) closeModal(loginModal);
        });
        loginModalContent.addEventListener('click', (e) => e.stopPropagation());
    }

    if (registerModal && registerModalContent) {
        registerModal.addEventListener('click', (e) => {
            if (e.target === registerModal) closeModal(registerModal);
        });
        registerModalContent.addEventListener('click', (e) => e.stopPropagation());
    }

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            if (loginModal && !loginModal.classList.contains('hidden')) {
                closeModal(loginModal);
            }
            if (registerModal && !registerModal.classList.contains('hidden')) {
                closeModal(registerModal);
            }
        }
    });

    const togglePassword = (field, openIcon, closedIcon) => {
        if (!field || !openIcon || !closedIcon) return;

        if (field.type === 'password') {
            field.type = 'text';
            openIcon.classList.add('hidden');
            closedIcon.classList.remove('hidden');
        } else {
            field.type = 'password';
            openIcon.classList.remove('hidden');
            closedIcon.classList.add('hidden');
        }
    };

    if (toggleLoginPasswordBtn && loginPasswordField && loginEyeOpen && loginEyeClosed) {
        toggleLoginPasswordBtn.addEventListener('click', () =>
            togglePassword(loginPasswordField, loginEyeOpen, loginEyeClosed)
        );
    }

    if (toggleRegisterPasswordBtn && registerPasswordField && registerEyeOpen && registerEyeClosed) {
        toggleRegisterPasswordBtn.addEventListener('click', () =>
            togglePassword(registerPasswordField, registerEyeOpen, registerEyeClosed)
        );
    }

});


function smoothScroll(targetId, duration = 1000) {
    const target = document.querySelector(targetId);
    if (!target) return;

    const targetPosition = target.getBoundingClientRect().top + window.pageYOffset;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;

    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const progress = Math.min(timeElapsed / duration, 1);
        const ease = easeInOutQuad(progress);

        window.scrollTo(0, startPosition + distance * ease);

        if (timeElapsed < duration) {
            requestAnimationFrame(animation);
        }
    }

    function easeInOutQuad(t) {
        return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    }

    requestAnimationFrame(animation);
}

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        smoothScroll(targetId, 1000);
    });
});