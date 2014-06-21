from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_solicitudes, votar, detalle_solicitud, finalizar_fase, finalizar_proyecto

urlpatterns = patterns('',
        url(r'^listar/$',listar_solicitudes, name='listar_solicitudes'),
        url(r'^votar/(?P<id_solicitud>\d+)$',votar, name='votar'),
        url(r'^votacion/(?P<id_solicitud>\d+)$',detalle_solicitud,name='detalle_solicitud'),
        url(r'^finalizacionFase/(?P<id_fase>\d+)$',finalizar_fase,name='finalizar_fase'),
        url(r'^finalizacionProyecto/(?P<id_proyecto>\d+)$',finalizar_proyecto,name='finalizar_proyecto'),
)
