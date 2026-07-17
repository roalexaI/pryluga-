from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from apps.tenants.models import Tenant, Sucursal


class Opcion(models.Model):
    codigo = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100)
    icono = models.CharField(max_length=50, blank=True)
    orden = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        ordering = ['orden']

    def __str__(self):
        return self.nombre


class Rol(models.Model):
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='roles'
    )
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    activo = models.BooleanField(default=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
        unique_together = ['tenant', 'nombre']
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} — {self.tenant.nombre}'

    def tiene_acceso(self, codigo_opcion):
        return self.permisos.filter(
            opcion__codigo=codigo_opcion,
            puede_ver=True,
            opcion__activo=True
        ).exists()


class RolPermiso(models.Model):
    rol = models.ForeignKey(
        Rol,
        on_delete=models.CASCADE,
        related_name='permisos'
    )
    opcion = models.ForeignKey(
        Opcion,
        on_delete=models.CASCADE,
        related_name='permisos'
    )
    puede_ver = models.BooleanField(default=False)
    puede_crear = models.BooleanField(default=False)
    puede_editar = models.BooleanField(default=False)
    puede_eliminar = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Permiso de Rol'
        verbose_name_plural = 'Permisos de Rol'
        unique_together = ['rol', 'opcion']

    def __str__(self):
        return f'{self.rol.nombre} — {self.opcion.nombre}'


class UsuarioManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin):

    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    rol = models.ForeignKey(
        Rol,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    sucursal = models.ForeignKey(
        Sucursal,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='usuarios'
    )
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    foto = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    activo = models.BooleanField(default=True)
    especialidad = models.CharField(max_length=200, blank=True)
    descripcion = models.TextField(blank=True)
    is_staff = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'

    @property
    def es_admin(self):
        return self.is_staff or self.is_superuser

    def tiene_acceso(self, codigo_opcion):
        if self.es_admin:
            return True
        if not self.rol:
            return False
        return self.rol.tiene_acceso(codigo_opcion)

    def puede(self, codigo_opcion, accion='ver'):
        if self.es_admin:
            return True
        if not self.rol:
            return False
        permiso = self.rol.permisos.filter(
            opcion__codigo=codigo_opcion,
            opcion__activo=True
        ).first()
        if not permiso:
            return False
        return getattr(permiso, f'puede_{accion}', False)