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
            background: '#141414',
            color: '#fff',
            iconColor: type === 'success' ? '#4caf50' : type === 'warning' ? '#f0b429' : '#e74c3c',
        });
    });
});

// ============================================================
// MARCAR ENLACE ACTIVO EN TOPBAR
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.sa-nav a');
    navLinks.forEach(function (link) {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});

// ============================================================
// CONFIRMAR ACCIONES CRÍTICAS (data-confirm)
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const formsConfirm = document.querySelectorAll('form[data-confirm]');
    formsConfirm.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            const msg = form.getAttribute('data-confirm');
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });
});

// ============================================================
// MODAL CREAR TENANT
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const tenantNombreInput = document.getElementById('tenantNombre');
    const tenantSlugInput = document.getElementById('tenantSlug');
    const btnConfirmarTenant = document.getElementById('btnConfirmarTenant');

    if (!btnConfirmarTenant) return;

    // Auto-generar slug
    if (tenantNombreInput && tenantSlugInput) {
        tenantNombreInput.addEventListener('input', function () {
            tenantSlugInput.value = this.value
                .toLowerCase()
                .replace(/\s+/g, '-')
                .replace(/[^a-z0-9-]/g, '');
        });
    }

    btnConfirmarTenant.addEventListener('click', function () {
        const nombre = tenantNombreInput.value.trim();
        if (!nombre) return;
        document.getElementById('confirmTenantNombre').textContent = nombre;
        bootstrap.Modal.getInstance(document.getElementById('modalCrearTenant')).hide();
        new bootstrap.Modal(document.getElementById('modalConfirmarTenant')).show();
    });

    document.getElementById('btnSubmitTenant').addEventListener('click', function () {
        document.getElementById('formCrearTenant').submit();
    });
});

// ============================================================
// MODAL CREAR SUCURSAL
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const modalSucursal = document.getElementById('modalCrearSucursal');
    if (!modalSucursal) return;

    modalSucursal.addEventListener('show.bs.modal', function (e) {
        const btn = e.relatedTarget;
        const tenantId = btn.getAttribute('data-tenant-id');
        const tenantNombre = btn.getAttribute('data-tenant-nombre');
        document.getElementById('sucursalTenantNombre').textContent = tenantNombre;
        document.getElementById('formCrearSucursal').action = `/superadmin/tenants/${tenantId}/sucursal/crear/`;
    });

    document.getElementById('btnConfirmarSucursal').addEventListener('click', function () {
        const nombre = document.querySelector('#formCrearSucursal input[name="nombre"]').value.trim();
        if (!nombre) return;
        document.getElementById('confirmSucursalNombre').textContent = nombre;
        bootstrap.Modal.getInstance(modalSucursal).hide();
        new bootstrap.Modal(document.getElementById('modalConfirmarSucursal')).show();
    });

    document.getElementById('btnSubmitSucursal').addEventListener('click', function () {
        document.getElementById('formCrearSucursal').submit();
    });
});

// ============================================================
// MODAL CREAR LICENCIA
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const modalLicencia = document.getElementById('modalCrearLicencia');
    if (!modalLicencia) return;

    modalLicencia.addEventListener('show.bs.modal', function (e) {
        const btn = e.relatedTarget;
        const tenantId = btn.getAttribute('data-tenant-id');
        const tenantNombre = btn.getAttribute('data-tenant-nombre');
        const sucursales = JSON.parse(btn.getAttribute('data-sucursales'));

        document.getElementById('licenciaTenantNombre').textContent = tenantNombre;
        document.getElementById('formCrearLicencia').action = `/superadmin/tenants/${tenantId}/licencia/crear/`;

        const select = document.getElementById('licenciaSucursal');
        select.innerHTML = '';
        sucursales.forEach(function (s) {
            const option = document.createElement('option');
            option.value = s.id;
            option.textContent = s.nombre;
            select.appendChild(option);
        });

        document.getElementById('licenciaFecha').value = new Date().toISOString().split('T')[0];
    });

    document.getElementById('btnConfirmarLicencia').addEventListener('click', function () {
        const sucursal = document.getElementById('licenciaSucursal');
        const fecha = document.getElementById('licenciaFecha').value;
        const monto = document.querySelector('#formCrearLicencia input[name="monto"]').value;
        if (!sucursal.value || !fecha) return;
        const texto = `${sucursal.options[sucursal.selectedIndex].text} — $${monto}/mes desde ${fecha}`;
        document.getElementById('confirmLicenciaDetalle').textContent = texto;
        bootstrap.Modal.getInstance(modalLicencia).hide();
        new bootstrap.Modal(document.getElementById('modalConfirmarLicencia')).show();
    });

    document.getElementById('btnSubmitLicencia').addEventListener('click', function () {
        document.getElementById('formCrearLicencia').submit();
    });
});

// ============================================================
// CREAR ROL — confirmar permisos
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const btnConfirmarRol = document.getElementById('btnConfirmarRol');
    if (!btnConfirmarRol) return;

    // Si marcan crear/editar/eliminar, auto-marcar ver
    document.querySelectorAll('.check-accion').forEach(function (check) {
        check.addEventListener('change', function () {
            if (this.checked) {
                const opcionId = this.getAttribute('data-opcion');
                const checkVer = document.querySelector(`.check-ver[data-opcion="${opcionId}"]`);
                if (checkVer) checkVer.checked = true;
            }
        });
    });

    btnConfirmarRol.addEventListener('click', function () {
        const nombre = document.querySelector('#formCrearRol input[name="nombre"]').value.trim();
        if (!nombre) return;
        document.getElementById('confirmRolNombre').textContent = nombre;
        new bootstrap.Modal(document.getElementById('modalConfirmarRol')).show();
    });

    document.getElementById('btnSubmitRol').addEventListener('click', function () {
        document.getElementById('formCrearRol').submit();
    });
});

// ============================================================
// CREAR USUARIO — confirmar
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const btnConfirmarUsuario = document.getElementById('btnConfirmarUsuario');
    if (!btnConfirmarUsuario) return;

    btnConfirmarUsuario.addEventListener('click', function () {
        const nombre = document.querySelector('#formCrearUsuario input[name="nombre"]').value.trim();
        const apellido = document.querySelector('#formCrearUsuario input[name="apellido"]').value.trim();
        const email = document.querySelector('#formCrearUsuario input[name="email"]').value.trim();
        if (!nombre || !apellido || !email) return;
        document.getElementById('confirmUsuarioNombre').textContent = `${nombre} ${apellido} — ${email}`;
        new bootstrap.Modal(document.getElementById('modalConfirmarUsuario')).show();
    });

    document.getElementById('btnSubmitUsuario').addEventListener('click', function () {
        document.getElementById('formCrearUsuario').submit();
    });
});


// ============================================================
// TREE TABLE TOGGLE
// ============================================================
function toggleTree(id) {
    const el = document.getElementById(id);
    const chevron = document.getElementById('chevron-' + id);
    if (!el) return;
    const isOpen = el.style.display !== 'none';
    el.style.display = isOpen ? 'none' : 'block';
    if (chevron) chevron.classList.toggle('open', !isOpen);
}

// ============================================================
// MODAL CREAR USUARIO (desde tenants tree)
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const modalCrearUsuario = document.getElementById('modalCrearUsuario');
    if (!modalCrearUsuario) return;

    modalCrearUsuario.addEventListener('show.bs.modal', function (e) {
        const btn = e.relatedTarget;
        const tenantId = btn.getAttribute('data-tenant-id');
        const tenantNombre = btn.getAttribute('data-tenant-nombre');
        const roles = JSON.parse(btn.getAttribute('data-roles') || '[]');
        const sucursales = JSON.parse(btn.getAttribute('data-sucursales') || '[]');

        document.getElementById('usuarioTenantNombre').textContent = tenantNombre;
        document.getElementById('formCrearUsuario').action = `/superadmin/tenants/${tenantId}/usuario/crear/`;

        const rolSelect = document.getElementById('usuarioRol');
        rolSelect.innerHTML = '<option value="">— Sin rol —</option>';
        roles.forEach(function (r) {
            rolSelect.innerHTML += `<option value="${r.id}">${r.nombre}</option>`;
        });

        const sucSelect = document.getElementById('usuarioSucursal');
        sucSelect.innerHTML = '<option value="">— Sin sucursal —</option>';
        sucursales.forEach(function (s) {
            sucSelect.innerHTML += `<option value="${s.id}">${s.nombre}</option>`;
        });
    });

    document.getElementById('btnConfirmarUsuarioModal').addEventListener('click', function () {
        const nombre = document.querySelector('#formCrearUsuario input[name="nombre"]').value.trim();
        const apellido = document.querySelector('#formCrearUsuario input[name="apellido"]').value.trim();
        if (!nombre || !apellido) return;
        document.getElementById('confirmUsuarioModalNombre').textContent = `${nombre} ${apellido}`;
        bootstrap.Modal.getInstance(modalCrearUsuario).hide();
        new bootstrap.Modal(document.getElementById('modalConfirmarUsuarioModal')).show();
    });

    document.getElementById('btnSubmitUsuarioModal').addEventListener('click', function () {
        document.getElementById('formCrearUsuario').submit();
    });
});

// ============================================================
// MODAL EDITAR USUARIO
// ============================================================
document.addEventListener('DOMContentLoaded', function () {
    const modalEditarUsuario = document.getElementById('modalEditarUsuario');
    if (!modalEditarUsuario) return;

    modalEditarUsuario.addEventListener('show.bs.modal', function (e) {
        const btn = e.relatedTarget;
        const usuarioId = btn.getAttribute('data-usuario-id');
        const roles = JSON.parse(btn.getAttribute('data-roles') || '[]');
        const sucursales = JSON.parse(btn.getAttribute('data-sucursales') || '[]');

        document.getElementById('editNombre').value = btn.getAttribute('data-nombre');
        document.getElementById('editApellido').value = btn.getAttribute('data-apellido');
        document.getElementById('editEmail').value = btn.getAttribute('data-email');
        document.getElementById('editTelefono').value = btn.getAttribute('data-telefono');
        document.getElementById('editActivo').checked = btn.getAttribute('data-activo') === 'true';
        document.getElementById('formEditarUsuario').action = `/superadmin/usuarios/${usuarioId}/editar/`;

        const rolActual = btn.getAttribute('data-rol');
        const rolSelect = document.getElementById('editRol');
        rolSelect.innerHTML = '<option value="">— Sin rol —</option>';
        roles.forEach(function (r) {
            rolSelect.innerHTML += `<option value="${r.id}" ${r.id == rolActual ? 'selected' : ''}>${r.nombre}</option>`;
        });

        const sucActual = btn.getAttribute('data-sucursal');
        const sucSelect = document.getElementById('editSucursal');
        sucSelect.innerHTML = '<option value="">— Sin sucursal —</option>';
        sucursales.forEach(function (s) {
            sucSelect.innerHTML += `<option value="${s.id}" ${s.id == sucActual ? 'selected' : ''}>${s.nombre}</option>`;
        });
    });

    document.getElementById('btnConfirmarEditarUsuario').addEventListener('click', function () {
        const nombre = document.getElementById('editNombre').value.trim();
        const apellido = document.getElementById('editApellido').value.trim();
        document.getElementById('confirmEditarUsuarioNombre').textContent = `${nombre} ${apellido}`;
        bootstrap.Modal.getInstance(modalEditarUsuario).hide();
        new bootstrap.Modal(document.getElementById('modalConfirmarEditarUsuario')).show();
    });

    document.getElementById('btnSubmitEditarUsuario').addEventListener('click', function () {
        document.getElementById('formEditarUsuario').submit();
    });
});