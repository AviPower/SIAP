__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_lineasBase, crear_lineaBase,detalle_lineabase

urlpatterns = patterns('',
        url(r'^listar/(?P<id_fase>\d+)$',listar_lineasBase, name='listar_lBase'),
        url(r'^crear/(?P<id_fase>\d+)$',crear_lineaBase,name='crear_lineaBase'),
        url(r'^detalle/(?P<id_lb>\d+)$',detalle_lineabase,name='detalle_lineabase'),
        )