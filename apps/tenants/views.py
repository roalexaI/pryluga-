from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
from apps.reservas.models import Reserva
from apps.accounts.models import Usuario
from apps.servicios.models import Servicio
from apps.finanzas.models import CuentaPorCobrar
from django.db.models import Sum


@login_required
def dashboard(request):
    tenant = request.tenant
    hoy = timezone.localdate()

    reservas_hoy = Reserva.objects.filter(
        tenant=tenant,
        fecha=hoy
    ).count()

    reservas_del_dia = Reserva.objects.filter(
        tenant=tenant,
        fecha=hoy
    ).select_related('cliente', 'especialista', 'servicio').order_by('hora_inicio')

    saldos_pendientes = CuentaPorCobrar.objects.filter(
        tenant=tenant,
        estado='pendiente'
    ).aggregate(total=Sum('monto_pendiente'))['total'] or 0

    total_clientes = Usuario.objects.filter(
        tenant=tenant,
        rol__nombre='Cliente',
        activo=True
    ).count()

    total_servicios = Servicio.objects.filter(
        tenant=tenant,
        activo=True
    ).count()

    return render(request, 'dashboard/index.html', {
        'reservas_hoy': reservas_hoy,
        'reservas_del_dia': reservas_del_dia,
        'saldos_pendientes': saldos_pendientes,
        'total_clientes': total_clientes,
        'total_servicios': total_servicios,
    })