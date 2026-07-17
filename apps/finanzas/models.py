from django.db import models
from apps.tenants.models import Tenant, Sucursal
from apps.reservas.models import Reserva


class Pago(models.Model):
    METODOS = [
        ('efectivo', 'Efectivo'),
        ('transferencia', 'Transferencia bancaria'),
        ('datafast', 'Datafast'),
    ]

    TIPOS = [
        ('anticipo', 'Anticipo'),
        ('pago_completo', 'Pago completo'),
        ('saldo', 'Saldo pendiente'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    reserva = models.ForeignKey(
        Reserva,
        on_delete=models.CASCADE,
        related_name='pagos'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    metodo = models.CharField(max_length=20, choices=METODOS)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    comprobante = models.ImageField(upload_to='pagos/comprobantes/', null=True, blank=True)
    observacion = models.TextField(blank=True)
    aprobado = models.BooleanField(default=False)
    aprobado_por = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='pagos_aprobados'
    )
    fecha_pago = models.DateTimeField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        ordering = ['-fecha_pago']

    def __str__(self):
        return f'{self.reserva.cliente.nombre_completo} — {self.get_tipo_display()} — ${self.monto}'


class Nomina(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='nominas'
    )
    especialista = models.ForeignKey(
        'accounts.Usuario',
        on_delete=models.CASCADE,
        related_name='nominas'
    )
    periodo_inicio = models.DateField()
    periodo_fin = models.DateField()
    sueldo_base = models.DecimalField(max_digits=10, decimal_places=2)
    comision_productos = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    observacion = models.TextField(blank=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Nómina'
        verbose_name_plural = 'Nóminas'
        ordering = ['-periodo_fin']

    def __str__(self):
        return f'{self.especialista.nombre_completo} — {self.periodo_inicio} al {self.periodo_fin}'

    def calcular_total(self):
        self.total = self.sueldo_base + self.comision_productos
        return self.total


class CuentaPorCobrar(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
        ('vencido', 'Vencido'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='cuentas_por_cobrar'
    )
    reserva = models.OneToOneField(
        Reserva,
        on_delete=models.CASCADE,
        related_name='cuenta_por_cobrar'
    )
    monto_total = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    monto_pendiente = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Cuenta por Cobrar'
        verbose_name_plural = 'Cuentas por Cobrar'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.reserva.cliente.nombre_completo} — ${self.monto_pendiente} pendiente'

    def actualizar_saldo(self):
        from django.db.models import Sum
        pagado = self.reserva.pagos.filter(aprobado=True).aggregate(
            total=Sum('monto')
        )['total'] or 0
        self.monto_pagado = pagado
        self.monto_pendiente = self.monto_total - pagado
        if self.monto_pendiente <= 0:
            self.estado = 'pagado'
        self.save()


class CuentaPorPagar(models.Model):
    TIPOS = [
        ('nomina', 'Nómina'),
        ('proveedor', 'Proveedor'),
        ('otro', 'Otro'),
    ]

    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='cuentas_por_pagar'
    )
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.CharField(max_length=300)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_vencimiento = models.DateField(null=True, blank=True)
    fecha_pago = models.DateTimeField(null=True, blank=True)
    nomina = models.ForeignKey(
        Nomina,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cuentas_por_pagar'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Cuenta por Pagar'
        verbose_name_plural = 'Cuentas por Pagar'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.get_tipo_display()} — {self.descripcion} — ${self.monto}'