from django.contrib import admin
from .models import Tenant, Sucursal


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