from django.contrib import admin
from .models import Factura


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ['numero_secuencial', 'razon_social_cliente', 'total', 'estado', 'fecha_emision']
    list_filter = ['estado', 'tenant']
    search_fields = ['numero_secuencial', 'razon_social_cliente', 'identificacion_cliente']
    date_hierarchy = 'fecha_emision'