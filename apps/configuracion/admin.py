from django.contrib import admin
from .models import (
    ConfiguracionNegocio, CuentaBancaria,
    ConfiguracionWhatsApp, PlantillaMensaje, ConfiguracionSRI
)


@admin.register(ConfiguracionNegocio)
class ConfiguracionNegocioAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'nombre_comercial', 'ruc', 'telefono']


@admin.register(CuentaBancaria)
class CuentaBancariaAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'banco', 'numero_cuenta', 'tipo_cuenta', 'titular', 'activo', 'orden']
    list_filter = ['activo', 'tenant', 'banco']


@admin.register(ConfiguracionWhatsApp)
class ConfiguracionWhatsAppAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'nombre', 'numero', 'activo']
    list_filter = ['activo', 'tenant']


@admin.register(PlantillaMensaje)
class PlantillaMensajeAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'tipo', 'dias_anticipacion', 'activo']
    list_filter = ['activo', 'tenant', 'tipo']


@admin.register(ConfiguracionSRI)
class ConfiguracionSRIAdmin(admin.ModelAdmin):
    list_display = ['tenant', 'ruc_emisor', 'razon_social', 'ambiente', 'activo']
    list_filter = ['activo', 'ambiente']