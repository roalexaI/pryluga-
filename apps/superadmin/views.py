from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from apps.tenants.models import Tenant, Sucursal, Licencia, PagoLicencia


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
    return render(request, 'superadmin/tenants.html', {
        'tenants': tenants,
    })


@superadmin_required
def licencias(request):
    licencias = Licencia.objects.select_related(
        'sucursal__tenant'
    ).order_by('-fecha_vencimiento')
    return render(request, 'superadmin/licencias.html', {
        'licencias': licencias,
    })


@superadmin_required
def pagos(request):
    pagos = PagoLicencia.objects.select_related(
        'sucursal__tenant'
    ).order_by('-fecha_subida')
    return render(request, 'superadmin/pagos.html', {
        'pagos': pagos,
    })


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

    return render(request, 'superadmin/pagos.html')


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

    return render(request, 'superadmin/pagos.html')