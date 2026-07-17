from django.contrib import admin
from .models import HorarioEspecialista, Reserva, RegresoTratamiento


@admin.register(HorarioEspecialista)
class HorarioEspecialistaAdmin(admin.ModelAdmin):
    list_display = ['especialista', 'sucursal', 'dia_semana', 'hora_inicio', 'hora_fin', 'activo']
    list_filter = ['activo', 'sucursal', 'dia_semana']
    search_fields = ['especialista__nombre', 'especialista__apellido']


@admin.register(Reserva)
class ReservaAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'especialista', 'servicio', 'fecha', 'hora_inicio', 'estado']
    list_filter = ['estado', 'sucursal', 'fecha']
    search_fields = ['cliente__nombre', 'cliente__apellido', 'especialista__nombre']
    date_hierarchy = 'fecha'


@admin.register(RegresoTratamiento)
class RegresoTratamientoAdmin(admin.ModelAdmin):
    list_display = ['reserva', 'fecha_regreso', 'dias_para_regresar', 'recordatorio_enviado']
    list_filter = ['recordatorio_enviado']