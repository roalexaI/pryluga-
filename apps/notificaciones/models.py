from django.db import models
from apps.tenants.models import Tenant
from apps.reservas.models import Reserva


class Notificacion(models.Model):
    TIPOS = [
        ('cita_proxima', 'Recordatorio de cita próxima'),
        ('saldo_pendiente', 'Recordatorio de saldo pendiente'),
        ('regreso_tratamiento', 'Recordatorio de regreso de tratamiento'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('enviado', 'Enviado'),
        ('fallido', 'Fallido'),
    ]

    CANALES = [
        ('whatsapp', 'WhatsApp'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    destinatario = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='notificaciones'
    )
    tipo = models.CharField(max_length=30, choices=TIPOS)
    canal = models.CharField(max_length=20, choices=CANALES, default='whatsapp')
    mensaje = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    numero_destino = models.CharField(max_length=20)
    fecha_programada = models.DateTimeField()
    fecha_envio = models.DateTimeField(null=True, blank=True)
    error = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Notificación'
        verbose_name_plural = 'Notificaciones'
        ordering = ['-fecha_programada']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.destinatario.nombre_completo} — {self.estado}'