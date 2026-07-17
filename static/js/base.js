// ============================================================
// MENSAJES DJANGO → SWEETALERT2 TOAST
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const messages = document.querySelectorAll('[data-message]');
    messages.forEach(function (el) {
        const type = el.getAttribute('data-type');
        const text = el.getAttribute('data-message');

        const iconMap = {
            'success': 'success',
            'error': 'error',
            'warning': 'warning',
            'info': 'info',
            'debug': 'info',
        };

        Swal.fire({
            toast: true,
            position: 'top-end',
            icon: iconMap[type] || 'info',
            title: text,
            showConfirmButton: false,
            timer: 4000,
            timerProgressBar: true,
            background: '#1a1a1a',
            color: '#fff',
            iconColor: type === 'success' ? '#8B6914' : type === 'warning' ? '#f0b429' : '#e74c3c',
        });
    });
});

// ============================================================
// MARCAR ENLACE ACTIVO EN TOPBAR
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.topbar-nav a, .mobile-menu a');
    navLinks.forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// ============================================================
// TOGGLE MENÚ MÓVIL
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const toggle = document.getElementById('mobileToggle');
    const menu = document.getElementById('mobileMenu');
    if (toggle && menu) {
        toggle.addEventListener('click', function () {
            menu.classList.toggle('open');
        });
    }
});