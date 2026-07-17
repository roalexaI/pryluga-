from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tenants/', views.tenants, name='tenants'),
    path('tenants/crear/', views.crear_tenant, name='crear_tenant'),
    path('tenants/<int:tenant_id>/sucursal/crear/', views.crear_sucursal, name='crear_sucursal'),
    path('tenants/<int:tenant_id>/usuario/crear/', views.crear_usuario, name='crear_usuario'),
    path('tenants/<int:tenant_id>/roles/', views.roles, name='roles'),
    path('tenants/<int:tenant_id>/roles/crear/', views.crear_rol, name='crear_rol'),
    path('tenants/<int:tenant_id>/licencia/crear/', views.crear_licencia, name='crear_licencia'),
    path('licencias/', views.licencias, name='licencias'),
    path('pagos/', views.pagos, name='pagos'),
    path('pagos/<int:pago_id>/aprobar/', views.aprobar_pago, name='aprobar_pago'),
    path('pagos/<int:pago_id>/rechazar/', views.rechazar_pago, name='rechazar_pago'),
]