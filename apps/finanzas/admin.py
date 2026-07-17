from django.contrib import admin
from .models import Pago, Nomina, CuentaPorCobrar, CuentaPorPagar


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ['reserva', 'tipo', 'metodo', 'monto', 'aprobado', 'fecha_pago']
    list_filter = ['tipo', 'metodo', 'aprobado', 'tenant']
    search_fields = ['reserva__cliente__nombre', 'reserva__cliente__apellido']
    date_hierarchy = 'fecha_pago'


@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ['especialista', 'periodo_inicio', 'periodo_fin', 'sueldo_base', 'comision_productos', 'total', 'estado']
    list_filter = ['estado', 'tenant']
    search_fields = ['especialista__nombre', 'especialista__apellido']


@admin.register(CuentaPorCobrar)
class CuentaPorCobrarAdmin(admin.ModelAdmin):
    list_display = ['reserva', 'monto_total', 'monto_pagado', 'monto_pendiente', 'estado']
    list_filter = ['estado', 'tenant']


@admin.register(CuentaPorPagar)
class CuentaPorPagarAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'descripcion', 'monto', 'estado', 'fecha_vencimiento']
    list_filter = ['tipo', 'estado', 'tenant']