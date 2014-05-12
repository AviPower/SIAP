__author__ = 'alvarenga'
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.contrib.auth.decorators import login_required, permission_required
admin.autodiscover()
from apps.tiposDeItem.views import listar_tiposItem, crear_tipoItem, detalle_tipoItem, listar_tiposItemProyecto, importar_tipoItem


urlpatterns = patterns('',
        url(r'^fase/(?P<id_fase>\d+)$',listar_tiposItem,name='listar_tiposItem' ),
        url(r'^registrar/(?P<id_fase>\d+)$',crear_tipoItem, name='crear_tipoItem'),
        url(r'^(?P<id_tipoItem>\d+)$', detalle_tipoItem, name='detalle_tipoItem'),
        url(r'^listar/(?P<id_fase>\d+)$',listar_tiposItemProyecto, name='listar_tiposItemProyecto'),
        url(r'^importar/(?P<id_tipoItem>\d+)-(?P<id_fase>\d+)$',importar_tipoItem, name='importar_tipoItem'),

)