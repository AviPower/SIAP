__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_lineasBase, crear_lineaBase,liberar_lineaBase

urlpatterns = patterns('',
        url(r'^listar/(?P<id_fase>\d+)$',listar_lineasBase, name='listar_lBase'),
        url(r'^crear/(?P<id_fase>\d+)$',crear_lineaBase,name='crear_lineaBase'),
        url(r'^liberar/(?P<id_fase>\d+)$',liberar_lineaBase,name='liberar_lineaBase'),
        )