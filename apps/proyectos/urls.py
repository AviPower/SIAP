__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_proyectos,registrar_proyecto, RegisterSuccessView, RegisterFailedView, detalle_proyecto, buscar_proyecto
from views import editar_proyecto
urlpatterns = patterns('',
        url(r'^registrar/$',registrar_proyecto, name='registrar_proyecto'),
        #Administracion de Proyectos
        url(r'^$',listar_proyectos, name='list_proyecto'),
        url(r'^(?P<id_proyecto>\d+)$', detalle_proyecto, name='detalle_proyecto'),
        url(r'^search/$',buscar_proyecto, name='buscar_proyectos'),
        url(r'^modificar/(?P<id_proyecto>\d+)$', editar_proyecto, name='edit_proyecto'),
        #url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', 'proyectos.views.cambiar_estado_proyecto'),
        #url(r'^importar/(?P<id_proyecto>\d+)$', 'proyectos.views.importar_proyecto'),
        #url(r'^equipo/(?P<id_proyecto>\d+)$', 'proyectos.views.ver_equipo'),
        url(r'^register/success/$',RegisterSuccessView ,name='RegisterSuccessView'),
        url(r'^register/failed/(?P<id_proyecto>\d+)$',RegisterFailedView, name='RegistroFallo')
        )