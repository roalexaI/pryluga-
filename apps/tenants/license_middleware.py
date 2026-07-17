from django.shortcuts import render
from django.utils import timezone


class LicenseMiddleware:

    RUTAS_EXENTAS = [
        '/auth/login/',
        '/auth/logout/',
        '/superadmin/',
        '/admin/',
        '/static/',
        '/media/',
        '/licencia/',
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        if request.user.is_superuser:
            return self.get_response(request)

        for ruta in self.RUTAS_EXENTAS:
            if request.path.startswith(ruta):
                return self.get_response(request)

        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return self.get_response(request)

        sucursal = getattr(request.user, 'sucursal', None)
        if not sucursal:
            return self.get_response(request)

        licencia = sucursal.licencias.filter(estado='activa').first()

        if not licencia or licencia.fecha_vencimiento < timezone.localdate():
            if request.method != 'GET':
                return render(request, 'licencia/vencida.html', {
                    'licencia': licencia,
                    'sucursal': sucursal,
                }, status=403)
            request.licencia_vencida = True
        else:
            request.licencia_vencida = False
            request.licencia = licencia

        return self.get_response(request)