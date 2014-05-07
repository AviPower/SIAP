__author__ = 'marcel'

from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_fases, registrar_fase
from views import editar_fase

urlpatterns = patterns('',
        #Administracion de Fases
        url(r'^registrar/(?P<id_proyecto>\d+)$',registrar_fase, name='registrar_fases'),
        url(r'^proyecto/(?P<id_proyecto>\d+)$', listar_fases, name='list_fase'),
        url(r'^editar/(?P<id_fase>\d+)$', editar_fase, name='edit_fase'),
        )