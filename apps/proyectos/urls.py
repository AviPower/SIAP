__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from apps.proyectos import views

urlpatterns = patterns('',
        #url(r'^registrar/$','proyectos.views.registrar_proyecto'),
        #Administracion de Proyectos
        url(r'^$','proyectos.views.listar_proyectos'),
        #url(r'^(?P<id_proyecto>\d+)$', 'proyectos.views.detalle_proyecto'),
        #url(r'^search/$',views.buscar_proyecto, name='buscar_proyectos'),
        #url(r'^modificar/(?P<id_proyecto>\d+)$', 'proyectos.views.editar_proyecto'),
        #url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', 'proyectos.views.cambiar_estado_proyecto'),
        #url(r'^importar/(?P<id_proyecto>\d+)$', 'proyectos.views.importar_proyecto'),
        #url(r'^equipo/(?P<id_proyecto>\d+)$', 'proyectos.views.ver_equipo'),
        #url(r'^register/success/$','proyectos.views.RegisterSuccessView'),
        #url(r'^register/failed/(?P<id_proyecto>\d+)$','proyectos.views.RegisterFailedView')
        )