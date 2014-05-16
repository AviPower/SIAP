__author__ = 'marcel'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_fases, registrar_fase, detalle_fase, buscar_fases, asignar_rol, asignar_usuario, asociar
from views import editar_fase,fases_todas, importar_fase, eliminar_fase, des, desasociar

urlpatterns = patterns('',
        #Administracion de Fases
        url(r'^registrar/(?P<id_proyecto>\d+)$',registrar_fase, name='registrar_fases'),
        url(r'^proyecto/(?P<id_proyecto>\d+)$', listar_fases, name='list_fase'),
        url(r'^editar/(?P<id_fase>\d+)$', editar_fase, name='edit_fase'),
        url(r'^lista_todas/(?P<id_proyecto>\d+)$',fases_todas,name='fases_todas'),
        url(r'^importar/(?P<id_fase>\d+)-(?P<id_proyecto>\d+)$', importar_fase,name='importar_fase'),
        url(r'^(?P<id_fase>\d+)$', detalle_fase, name='detalle_fase'),
        url(r'^eliminar/(?P<id_fase>\d+)$', eliminar_fase, name='eliminar_fase'),
        url(r'^search/(?P<id_proyecto>\d+)$',buscar_fases, name='buscar_fases'),
        url(r'^asignar/(?P<id_fase>\d+)$', asignar_usuario, name='asignar_usuario'),
        url(r'^asignar/(?P<id_usuario>\d+)/(?P<id_fase>\d+)$', asignar_rol, name='asignar_rol'),
        url(r'^asociar/(?P<id_rol>\d+)-(?P<id_usuario>\d+)-(?P<id_fase>\d+)$', asociar,name='asociar'),
        url(r'^des/(?P<id_fase>\d+)$', des, name='des'),
        url(r'^desasignar/(?P<id_usuario>\d+)/(?P<id_fase>\d+)$', desasociar,name='desasociar'),
        )