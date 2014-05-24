__author__ = 'teaser'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_solicitudes,registrar_solicitud, RegisterSuccessView, RegisterFailedView, detalle_solicitud, buscar_solicitud
#from views import editar_solicitud, cambiar_estado_solicitud

urlpatterns = patterns('',
        url(r'^registrar/$',registrar_solicitud, name='registrar_solicitud'),
        #Administracion de Solicitudes de Cambio
        url(r'^$',listar_solicitudes, name='listar_solicitudes'),
        url(r'^(?P<id_solicitud>\d+)$', detalle_solicitud, name='detalle_solicitud'),
        url(r'^search/$',buscar_solicitud, name='buscar_solicitud'),
       # url(r'^modificar/(?P<id_proyecto>\d+)$', editar_solicitud, name='editar_solicitud'),
       # url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', cambiar_estado_solicitud, name='cambiar_estado_solicitud'),
        url(r'^register/success/$',RegisterSuccessView ,name='RegisterSuccessView'),
        url(r'^register/failed/(?P<id_solicitud>\d+)$',RegisterFailedView, name='RegistroFallo')
)
