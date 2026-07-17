from django.contrib import admin
from .models import CategoriaServicio, Servicio, EspecialistaServicio


@admin.register(CategoriaServicio)
class CategoriaServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'tenant', 'orden', 'activo']
    list_filter = ['activo', 'tenant']
    search_fields = ['nombre']


@admin.register(Servicio)
class ServicioAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'precio', 'duracion_estimada', 'requiere_anticipo', 'activo']
    list_filter = ['activo', 'tenant', 'categoria', 'requiere_anticipo']
    search_fields = ['nombre']


@admin.register(EspecialistaServicio)
class EspecialistaServicioAdmin(admin.ModelAdmin):
    list_display = ['especialista', 'servicio', 'sucursal', 'activo']
    list_filter = ['activo', 'sucursal']