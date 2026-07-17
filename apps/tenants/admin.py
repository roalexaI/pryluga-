from django.contrib import admin
from .models import Tenant, Sucursal, Licencia, PagoLicencia


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'slug', 'activo', 'fecha_creacion']
    prepopulated_fields = {'slug': ('nombre',)}
    list_filter = ['activo']
    search_fields = ['nombre']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tenant', 'es_principal', 'activo']
    list_filter = ['activo', 'tenant', 'es_principal']
    search_fields = ['nombre']


@admin.register(Licencia)
class LicenciaAdmin(admin.ModelAdmin):
    list_display = ['sucursal', 'fecha_activacion', 'fecha_vencimiento', 'monto', 'estado', 'dias_restantes']
    list_filter = ['estado', 'sucursal__tenant']
    search_fields = ['sucursal__nombre']


@admin.register(PagoLicencia)
class PagoLicenciaAdmin(admin.ModelAdmin):
    list_display = ['sucursal', 'monto', 'estado', 'fecha_pago', 'fecha_subida']
    list_filter = ['estado', 'sucursal__tenant']
    search_fields = ['sucursal__nombre']