from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from apps.tenants.models import Tenant, Sucursal, Licencia, PagoLicencia
from apps.accounts.models import Usuario, Rol, Opcion, RolPermiso


def superadmin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return redirect('/auth/login/')
        return view_func(request, *args, **kwargs)
    return wrapper


@superadmin_required
def dashboard(request):
    total_tenants = Tenant.objects.filter(activo=True).count()
    total_sucursales = Sucursal.objects.filter(activo=True).count()
    hoy = timezone.localdate()

    proximas_a_vencer = Licencia.objects.filter(
        estado='activa',
        fecha_vencimiento__lte=hoy + timedelta(days=5),
        fecha_vencimiento__gte=hoy
    ).select_related('sucursal__tenant')

    vencidas = Licencia.objects.filter(
        estado='activa',
        fecha_vencimiento__lt=hoy
    ).select_related('sucursal__tenant')

    pagos_pendientes = PagoLicencia.objects.filter(
        estado='pendiente'
    ).select_related('sucursal__tenant')

    return render(request, 'superadmin/dashboard.html', {
        'total_tenants': total_tenants,
        'total_sucursales': total_sucursales,
        'proximas_a_vencer': proximas_a_vencer,
        'vencidas': vencidas,
        'pagos_pendientes': pagos_pendientes,
    })


@superadmin_required
def tenants(request):
    tenants = Tenant.objects.prefetch_related('sucursales__licencias').all()
    return render(request, 'superadmin/tenants.html', {'tenants': tenants})


@superadmin_required
def crear_tenant(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        slug = request.POST.get('slug')
        if nombre and slug:
            tenant = Tenant.objects.create(nombre=nombre, slug=slug)
            messages.success(request, f'Tenant "{tenant.nombre}" creado correctamente.')
            return redirect('/superadmin/tenants/')
        messages.error(request, 'Nombre y slug son obligatorios.')
    return render(request, 'superadmin/crear_tenant.html')


@superadmin_required
def crear_sucursal(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        direccion = request.POST.get('direccion')
        telefono = request.POST.get('telefono', '')
        email = request.POST.get('email', '')
        es_principal = request.POST.get('es_principal') == 'on'
        if nombre and direccion:
            sucursal = Sucursal.objects.create(
                tenant=tenant,
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                email=email,
                es_principal=es_principal,
            )
            messages.success(request, f'Sucursal "{sucursal.nombre}" creada.')
            return redirect('/superadmin/tenants/')
        messages.error(request, 'Nombre y dirección son obligatorios.')
    return render(request, 'superadmin/crear_sucursal.html', {'tenant': tenant})


@superadmin_required
def crear_licencia(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    sucursales = tenant.sucursales.filter(activo=True)
    if request.method == 'POST':
        sucursal_id = request.POST.get('sucursal')
        fecha_activacion = request.POST.get('fecha_activacion')
        monto = request.POST.get('monto', 80)
        sucursal = get_object_or_404(Sucursal, id=sucursal_id, tenant=tenant)
        from datetime import date
        fecha = date.fromisoformat(fecha_activacion)
        licencia = Licencia.objects.create(
            sucursal=sucursal,
            fecha_activacion=fecha,
            fecha_vencimiento=fecha + timedelta(days=30),
            monto=monto,
            estado='activa',
            activada_por=request.user,
        )
        messages.success(request, f'Licencia creada. Vence el {licencia.fecha_vencimiento}.')
        return redirect('/superadmin/tenants/')
    return render(request, 'superadmin/crear_licencia.html', {
        'tenant': tenant,
        'sucursales': sucursales,
        'hoy': timezone.localdate(),
    })


@superadmin_required
def crear_usuario(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    roles = Rol.objects.filter(tenant=tenant)
    sucursales = tenant.sucursales.filter(activo=True)
    if request.method == 'POST':
        email = request.POST.get('email')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        telefono = request.POST.get('telefono', '')
        password = request.POST.get('password')
        rol_id = request.POST.get('rol')
        sucursal_id = request.POST.get('sucursal')
        rol = get_object_or_404(Rol, id=rol_id) if rol_id else None
        sucursal = get_object_or_404(Sucursal, id=sucursal_id) if sucursal_id else None
        if email and nombre and apellido and password:
            usuario = Usuario.objects.create_user(
                email=email,
                password=password,
                nombre=nombre,
                apellido=apellido,
                telefono=telefono,
                tenant=tenant,
                rol=rol,
                sucursal=sucursal,
            )
            messages.success(request, f'Usuario {usuario.nombre_completo} creado.')
            return redirect('/superadmin/tenants/')
        messages.error(request, 'Todos los campos son obligatorios.')
    return render(request, 'superadmin/crear_usuario.html', {
        'tenant': tenant,
        'roles': roles,
        'sucursales': sucursales,
    })


@superadmin_required
def roles(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    roles = Rol.objects.filter(tenant=tenant)
    return render(request, 'superadmin/roles.html', {
        'tenant': tenant,
        'roles': roles,
    })


@superadmin_required
def crear_rol(request, tenant_id):
    tenant = get_object_or_404(Tenant, id=tenant_id)
    opciones = Opcion.objects.filter(activo=True).order_by('orden')
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion', '')
        if nombre:
            rol = Rol.objects.create(
                tenant=tenant,
                nombre=nombre,
                descripcion=descripcion,
            )
            for opcion in opciones:
                puede_ver = request.POST.get(f'ver_{opcion.id}') == 'on'
                puede_crear = request.POST.get(f'crear_{opcion.id}') == 'on'
                puede_editar = request.POST.get(f'editar_{opcion.id}') == 'on'
                puede_eliminar = request.POST.get(f'eliminar_{opcion.id}') == 'on'
                if any([puede_ver, puede_crear, puede_editar, puede_eliminar]):
                    RolPermiso.objects.create(
                        rol=rol,
                        opcion=opcion,
                        puede_ver=puede_ver,
                        puede_crear=puede_crear,
                        puede_editar=puede_editar,
                        puede_eliminar=puede_eliminar,
                    )
            messages.success(request, f'Rol "{rol.nombre}" creado con permisos.')
            return redirect('/superadmin/tenants/')
        messages.error(request, 'El nombre es obligatorio.')
    return render(request, 'superadmin/crear_rol.html', {
        'tenant': tenant,
        'opciones': opciones,
    })


@superadmin_required
def licencias(request):
    licencias = Licencia.objects.select_related(
        'sucursal__tenant'
    ).order_by('-fecha_vencimiento')
    return render(request, 'superadmin/licencias.html', {'licencias': licencias})


@superadmin_required
def pagos(request):
    pagos = PagoLicencia.objects.select_related(
        'sucursal__tenant'
    ).order_by('-fecha_subida')
    return render(request, 'superadmin/pagos.html', {'pagos': pagos})


@superadmin_required
def aprobar_pago(request, pago_id):
    pago = get_object_or_404(PagoLicencia, id=pago_id)
    if request.method == 'POST':
        hoy = timezone.localdate()
        licencia_activa = pago.sucursal.licencias.filter(estado='activa').first()
        if licencia_activa and licencia_activa.fecha_vencimiento >= hoy:
            fecha_inicio = licencia_activa.fecha_vencimiento + timedelta(days=1)
        else:
            fecha_inicio = hoy
        nueva_licencia = Licencia.objects.create(
            sucursal=pago.sucursal,
            fecha_activacion=fecha_inicio,
            fecha_vencimiento=fecha_inicio + timedelta(days=30),
            monto=pago.monto,
            estado='activa',
            activada_por=request.user,
        )
        pago.estado = 'aprobado'
        pago.licencia = nueva_licencia
        pago.revisado_por = request.user
        pago.fecha_revision = timezone.now()
        pago.observacion_admin = request.POST.get('observacion', '')
        pago.save()
        messages.success(request, f'Pago aprobado. Licencia activa hasta {nueva_licencia.fecha_vencimiento}.')
        return redirect('/superadmin/pagos/')
    return redirect('/superadmin/pagos/')


@superadmin_required
def rechazar_pago(request, pago_id):
    pago = get_object_or_404(PagoLicencia, id=pago_id)
    if request.method == 'POST':
        pago.estado = 'rechazado'
        pago.revisado_por = request.user
        pago.fecha_revision = timezone.now()
        pago.observacion_admin = request.POST.get('observacion', '')
        pago.save()
        messages.warning(request, 'Pago rechazado.')
        return redirect('/superadmin/pagos/')
    return redirect('/superadmin/pagos/')