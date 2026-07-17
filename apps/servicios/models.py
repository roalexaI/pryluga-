from django.db import models
from apps.tenants.models import Tenant, Sucursal


class CategoriaServicio(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='categorias_servicio'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='servicios/categorias/', null=True, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categoría de Servicio'
        verbose_name_plural = 'Categorías de Servicio'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='servicios'
    )
    categoria = models.ForeignKey(
        CategoriaServicio,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='servicios'
    )
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='servicios/', null=True, blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    duracion_estimada = models.PositiveIntegerField(help_text='Duración en minutos')
    requiere_anticipo = models.BooleanField(default=False)
    porcentaje_anticipo = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.00,
        help_text='Porcentaje de anticipo requerido'
    )
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Servicio'
        verbose_name_plural = 'Servicios'
        ordering = ['orden', 'nombre']

    def __str__(self):
        return f'{self.nombre} — ${self.precio}'


class EspecialistaServicio(models.Model):
    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE,
        related_name='especialistas'
    )
    especialista = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='servicios_asignados'
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.CASCADE,
        related_name='especialista_servicios'
    )
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Especialista por Servicio'
        verbose_name_plural = 'Especialistas por Servicio'
        unique_together = ['servicio', 'especialista', 'sucursal']

    def __str__(self):
        return f'{self.especialista.nombre_completo} — {self.servicio.nombre}'