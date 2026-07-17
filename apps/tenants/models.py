from django.db import models
from django.utils import timezone
from datetime import timedelta


class Tenant(models.Model):
    nombre = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Sucursal(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='sucursales'
    )
    nombre = models.CharField(max_length=200)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    es_principal = models.BooleanField(default=False)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'
        ordering = ['-es_principal', 'nombre']

    def __str__(self):
        return f'{self.tenant.nombre} — {self.nombre}'

    @property
    def licencia_activa(self):
        return self.licencias.filter(estado='activa').first()

    @property
    def licencia_vencida(self):
        licencia = self.licencia_activa
        if not licencia:
            return True
        return licencia.fecha_vencimiento < timezone.localdate()


class Licencia(models.Model):
    ESTADOS = [
        ('activa', 'Activa'),
        ('vencida', 'Vencida'),
        ('suspendida', 'Suspendida'),
        ('pendiente', 'Pendiente de pago'),
    ]

    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='licencias'
    )
    fecha_activacion = models.DateField()
    fecha_vencimiento = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=80.00)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    activada_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='licencias_activadas'
    )
    observacion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Licencia'
        verbose_name_plural = 'Licencias'
        ordering = ['-fecha_vencimiento']

    def __str__(self):
        return f'{self.sucursal} — {self.get_estado_display()} — vence {self.fecha_vencimiento}'

    def save(self, *args, **kwargs):
        if not self.fecha_vencimiento:
            self.fecha_vencimiento = self.fecha_activacion + timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def dias_restantes(self):
        delta = self.fecha_vencimiento - timezone.localdate()
        return delta.days

    @property
    def proxima_a_vencer(self):
        return 0 <= self.dias_restantes <= 5


class PagoLicencia(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente de revisión'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]

    licencia = models.ForeignKey(
        Licencia,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='pagos'
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='pagos_licencia'
    )
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=80.00)
    comprobante = models.ImageField(upload_to='licencias/comprobantes/')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observacion_cliente = models.TextField(blank=True)
    observacion_admin = models.TextField(blank=True)
    revisado_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos_licencia_revisados'
    )
    fecha_pago = models.DateField()
    fecha_subida = models.DateTimeField(auto_now_add=True)
    fecha_revision = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = 'Pago de Licencia'
        verbose_name_plural = 'Pagos de Licencia'
        ordering = ['-fecha_subida']

    def __str__(self):
        return f'{self.sucursal} — ${self.monto} — {self.get_estado_display()}'