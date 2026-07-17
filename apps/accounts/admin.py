from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Rol, RolPermiso, Opcion

@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'orden', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'codigo']

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tenant', 'activo', 'fecha_creacion']
    list_filter = ['activo', 'tenant']
    search_fields = ['nombre']

@admin.register(RolPermiso)
class RolPermisoAdmin(admin.ModelAdmin):
    list_display = ['rol', 'opcion', 'puede_ver', 'puede_crear', 'puede_editar', 'puede_eliminar']
    list_filter = ['rol', 'opcion']

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['email', 'nombre', 'apellido', 'rol', 'tenant', 'activo']
    list_filter = ['activo', 'tenant', 'rol']
    search_fields = ['email', 'nombre', 'apellido']
    ordering = ['nombre']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información personal', {'fields': ('nombre', 'apellido', 'telefono', 'foto')}),
        ('Rol y acceso', {'fields': ('tenant', 'rol', 'activo', 'especialidad', 'descripcion')}),
        ('Permisos', {'fields': ('is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido', 'tenant', 'rol', 'password1', 'password2'),
        }),
    )