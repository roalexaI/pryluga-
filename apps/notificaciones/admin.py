from django.contrib import admin
from .models import Notificacion


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'destinatario', 'canal', 'estado', 'fecha_programada', 'fecha_envio']
    list_filter = ['tipo', 'canal', 'estado', 'tenant']
    search_fields = ['destinatario__nombre', 'destinatario__apellido', 'numero_destino']
    date_hierarchy = 'fecha_programada'