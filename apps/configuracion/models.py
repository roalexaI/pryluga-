from django.db import models
from apps.tenants.models import Tenant


class ConfiguracionNegocio(models.Model):
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name='configuracion'
    )
    nombre_comercial = models.CharField(max_length=200)
    ruc = models.CharField(max_length=13)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    email = models.EmailField()
    logo = models.ImageField(upload_to='configuracion/logos/', null=True, blank=True)
    slogan = models.CharField(max_length=300, blank=True)
    instagram = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    tiktok = models.URLField(blank=True)
    whatsapp = models.CharField(max_length=20, blank=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración del Negocio'
        verbose_name_plural = 'Configuración del Negocio'

    def __str__(self):
        return f'Configuración — {self.tenant.nombre}'


class CuentaBancaria(models.Model):
    TIPOS = [
        ('ahorros', 'Ahorros'),
        ('corriente', 'Corriente'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='cuentas_bancarias'
    )
    banco = models.CharField(max_length=100)
    numero_cuenta = models.CharField(max_length=50)
    tipo_cuenta = models.CharField(max_length=20, choices=TIPOS)
    titular = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    orden = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = 'Cuenta Bancaria'
        verbose_name_plural = 'Cuentas Bancarias'
        ordering = ['orden']

    def __str__(self):
        return f'{self.banco} — {self.numero_cuenta}'


class ConfiguracionWhatsApp(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='configuraciones_whatsapp'
    )
    nombre = models.CharField(max_length=100)
    numero = models.CharField(max_length=20)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Número de WhatsApp'
        verbose_name_plural = 'Números de WhatsApp'

    def __str__(self):
        return f'{self.nombre} — {self.numero}'


class PlantillaMensaje(models.Model):
    TIPOS = [
        ('cita_proxima', 'Recordatorio de cita próxima'),
        ('saldo_pendiente', 'Recordatorio de saldo pendiente'),
        ('regreso_tratamiento', 'Recordatorio de regreso de tratamiento'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='plantillas_mensaje'
    )
    tipo = models.CharField(max_length=50, choices=TIPOS)
    mensaje = models.TextField()
    dias_anticipacion = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Plantilla de Mensaje'
        verbose_name_plural = 'Plantillas de Mensajes'
        unique_together = ['tenant', 'tipo']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.tenant.nombre}'


class ConfiguracionSRI(models.Model):
    AMBIENTES = [
        ('1', 'Pruebas'),
        ('2', 'Producción'),
    ]

    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name='configuracion_sri'
    )
    ruc_emisor = models.CharField(max_length=13)
    razon_social = models.CharField(max_length=300)
    nombre_comercial = models.CharField(max_length=300, blank=True)
    direccion_matriz = models.TextField()
    codigo_establecimiento = models.CharField(max_length=3, default='001')
    codigo_punto_emision = models.CharField(max_length=3, default='001')
    ambiente = models.CharField(max_length=1, choices=AMBIENTES, default='1')
    certificado_p12 = models.FileField(upload_to='configuracion/sri/', null=True, blank=True)
    clave_certificado = models.CharField(max_length=200, blank=True)
    secuencial_factura = models.PositiveIntegerField(default=1)
    activo = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Configuración SRI'
        verbose_name_plural = 'Configuración SRI'

    def __str__(self):
        return f'SRI — {self.tenant.nombre}'