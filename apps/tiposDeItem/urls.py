__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from apps.tiposDeItem.views import listar_tiposItem, crear_tipoItem, detalle_tipoItem, listar_tiposItemProyecto, importar_tipoItem
from apps.tiposDeItem.views import eliminar_tipoItem, editar_tipoItem, crear_atributo, eliminar_atributo, modificar_atributo, buscar_tiposItem

urlpatterns = patterns('',
        url(r'^fase/(?P<id_fase>\d+)$',listar_tiposItem,name='listar_tiposItem' ),
        url(r'^registrar/(?P<id_fase>\d+)$',crear_tipoItem, name='crear_tipoItem'),
        url(r'^(?P<id_tipoItem>\d+)$', detalle_tipoItem, name='detalle_tipoItem'),
        url(r'^listar/(?P<id_fase>\d+)$',listar_tiposItemProyecto, name='listar_tiposItemProyecto'),
        url(r'^importar/(?P<id_tipoItem>\d+)-(?P<id_fase>\d+)$',importar_tipoItem, name='importar_tipoItem'),
        url(r'^eliminar/(?P<id_tipoItem>\d+)$',eliminar_tipoItem, name='eliminar_tipoItem'),
        url(r'^modificar/(?P<id_tipoItem>\d+)$', editar_tipoItem,name='editar_tipoItem'),
        url(r'^(?P<id_tipoItem>\d+)/crear_atributo$', crear_atributo, name='crear_atributo'),
        url(r'^eliminar/tipo_atributo/(?P<id_atributo>\d+)-(?P<id_tipoItem>\d+)$',eliminar_atributo, name='eliminar_atributo'),
        url(r'^modificar/tipo_atributo/(?P<id_atributo>\d+)-(?P<id_tipoItem>\d+)$',modificar_atributo, name='modificar_atributo'),
        url(r'^search/(?P<id_fase>\d+)$',buscar_tiposItem, name='buscar_tiposItem')

)