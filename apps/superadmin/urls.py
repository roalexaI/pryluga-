from django.urls import path
from . import views

app_name = 'superadmin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('tenants/', views.tenants, name='tenants'),
    path('licencias/', views.licencias, name='licencias'),
    path('pagos/', views.pagos, name='pagos'),
    path('pagos/<int:pago_id>/aprobar/', views.aprobar_pago, name='aprobar_pago'),
    path('pagos/<int:pago_id>/rechazar/', views.rechazar_pago, name='rechazar_pago'),
]