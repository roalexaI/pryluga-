from django.shortcuts import redirect
from apps.tenants.models import Tenant


class TenantMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            tenant = Tenant.objects.filter(activo=True).first()
            request.tenant = tenant
        except Exception:
            request.tenant = None
        response = self.get_response(request)
        return response