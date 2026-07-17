def tenant_context(request):
    opciones = []

    if request.user.is_authenticated:
        if request.user.es_admin:
            from apps.accounts.models import Opcion
            opciones = Opcion.objects.filter(activo=True).order_by('orden')
        elif request.user.rol:
            opciones = [
                permiso.opcion
                for permiso in request.user.rol.permisos.filter(
                    puede_ver=True,
                    opcion__activo=True
                ).select_related('opcion').order_by('opcion__orden')
            ]

    return {
        'tenant': getattr(request, 'tenant', None),
        'opciones_menu': opciones,
    }