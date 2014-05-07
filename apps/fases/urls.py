__author__ = 'marcel'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_fases, registrar_fase#, #RegisterSuccessView, RegisterFailedView, detalle_proyecto, buscar_proyecto
from views import editar_fase #, importar_proyecto, ver_equipo, cambiar_estado_proyecto

urlpatterns = patterns('',
        url(r'^registrar/$',registrar_fase, name='registrar_fases'),
        #Administracion de Proyectos
        url(r'^$', listar_fases, name='list_fase'),
        #url(r'^(?P<id_proyecto>\d+)$', detalle_proyecto, name='detalle_proyecto'),
        #url(r'^search/$',buscar_proyecto, name='buscar_proyectos'),
       url(r'^editar/(?P<id_fase>\d+)$', editar_fase, name='edit_fase'),
       # url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', cambiar_estado_proyecto, name='camb_est_proyect'),
       # url(r'^importar/(?P<id_proyecto>\d+)$', importar_proyecto, name='importar_proyecto'),
       # url(r'^equipo/(?P<id_proyecto>\d+)$', ver_equipo, name='equipo'),
       ## url(r'^register/failed/(?P<id_proyecto>\d+)$',RegisterFailedView, name='RegistroFallo')
        )