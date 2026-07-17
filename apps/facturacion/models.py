from django.db import models
from apps.tenants.models import Tenant
from apps.finanzas.models import Pago


class Factura(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('emitida', 'Emitida'),
        ('autorizada', 'Autorizada'),
        ('anulada', 'Anulada'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='facturas'
    )
    pago = models.OneToOneField(
        Pago,
        on_delete=models.CASCADE,
        related_name='factura'
    )
    numero_secuencial = models.CharField(max_length=20)
    clave_acceso = models.CharField(max_length=49, blank=True)
    numero_autorizacion = models.CharField(max_length=49, blank=True)
    fecha_emision = models.DateTimeField()
    fecha_autorizacion = models.DateTimeField(null=True, blank=True)

    # Datos del cliente en el momento de la factura
    razon_social_cliente = models.CharField(max_length=300)
    identificacion_cliente = models.CharField(max_length=20)
    direccion_cliente = models.TextField(blank=True)
    email_cliente = models.EmailField(blank=True)

    # Valores
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    xml_generado = models.TextField(blank=True)
    pdf = models.FileField(upload_to='facturas/pdf/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Factura'
        verbose_name_plural = 'Facturas'
        ordering = ['-fecha_emision']

    def __str__(self):
        return f'Factura {self.numero_secuencial} — {self.razon_social_cliente}'