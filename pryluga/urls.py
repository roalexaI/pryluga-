from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('apps.core.urls')),
                  path('auth/', include('apps.accounts.urls')),
                  path('dashboard/', include('apps.tenants.urls')),
                  path('configuracion/', include('apps.configuracion.urls')),
                  path('servicios/', include('apps.servicios.urls')),
                  path('reservas/', include('apps.reservas.urls')),
                  path('agenda/', include('apps.agenda.urls')),
                  path('finanzas/', include('apps.finanzas.urls')),
                  path('facturacion/', include('apps.facturacion.urls')),
                  path('notificaciones/', include('apps.notificaciones.urls')),
                  path('notificaciones/', include('apps.notificaciones.urls')),
                  path('superadmin/', include('apps.superadmin.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
