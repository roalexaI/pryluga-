from django.db import models
from apps.tenants.models import Tenant, Sucursal
from apps.servicios.models import Servicio


class HorarioEspecialista(models.Model):
    DIAS = [
        (0, 'Lunes'),
        (1, 'Martes'),
        (2, 'Miércoles'),
        (3, 'Jueves'),
        (4, 'Viernes'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    especialista = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='horarios'
    )
    dia_semana = models.IntegerField(choices=DIAS)
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Horario de Especialista'
        verbose_name_plural = 'Horarios de Especialistas'
        unique_together = ['especialista', 'sucursal', 'dia_semana']
        ordering = ['dia_semana', 'hora_inicio']

    def __str__(self):
        return f'{self.especialista.nombre_completo} — {self.get_dia_semana_display()} {self.hora_inicio}–{self.hora_fin}'


class Reserva(models.Model):
    ESTADO_PENDIENTE = 'pendiente'
    ESTADO_CONFIRMADA = 'confirmada'
    ESTADO_EN_PROCESO = 'en_proceso'
    ESTADO_COMPLETADA = 'completada'
    ESTADO_CANCELADA = 'cancelada'
    ESTADO_NO_ASISTIO = 'no_asistio'

    ESTADOS = [
        (ESTADO_PENDIENTE, 'Pendiente'),
        (ESTADO_CONFIRMADA, 'Confirmada'),
        (ESTADO_EN_PROCESO, 'En proceso'),
        (ESTADO_COMPLETADA, 'Completada'),
        (ESTADO_CANCELADA, 'Cancelada'),
        (ESTADO_NO_ASISTIO, 'No asistió'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    cliente = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='reservas_cliente'
    )
    especialista = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='reservas_especialista'
    )
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='reservas'
    )
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin_estimada = models.TimeField()
    hora_inicio_real = models.TimeField(null=True, blank=True)
    hora_fin_real = models.TimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default=ESTADO_PENDIENTE)
    observaciones = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reserva'
        verbose_name_plural = 'Reservas'
        ordering = ['-fecha', '-hora_inicio']

    def __str__(self):
        return f'{self.cliente.nombre_completo} — {self.servicio.nombre} — {self.fecha}'

    @property
    def duracion_real(self):
        if self.hora_inicio_real and self.hora_fin_real:
            from datetime import datetime, date
            inicio = datetime.combine(date.today(), self.hora_inicio_real)
            fin = datetime.combine(date.today(), self.hora_fin_real)
            return int((fin - inicio).total_seconds() / 60)
        return None


class RegresoTratamiento(models.Model):
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='regresos'
    )
    dias_para_regresar = models.PositiveIntegerField()
    fecha_regreso = models.DateField()
    observacion = models.TextField(blank=True)
    recordatorio_enviado = models.BooleanField(default=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Regreso de Tratamiento'
        verbose_name_plural = 'Regresos de Tratamiento'

    def __str__(self):
        return f'{self.reserva.cliente.nombre_completo} — regreso {self.fecha_regreso}'