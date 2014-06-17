from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_solicitudes, votar, detalle_solicitud

urlpatterns = patterns('',
        url(r'^listar/$',listar_solicitudes, name='listar_solicitudes'),
        url(r'^votar/(?P<id_solicitud>\d+)$',votar, name='votar'),
        url(r'^votacion/(?P<id_solicitud>\d+)$',detalle_solicitud,name='detalle_solicitud'),
)
