__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from views import listar_proyectos,registrar_proyecto, RegisterSuccessView, RegisterFailedView

urlpatterns = patterns('',
        url(r'^registrar/$',registrar_proyecto, name='registrar_proyecto'),
        #Administracion de Proyectos
        url(r'^$',listar_proyectos, name='list_proyecto'),
        #url(r'^(?P<id_proyecto>\d+)$', 'proyectos.views.detalle_proyecto'),
        #url(r'^search/$',views.buscar_proyecto, name='buscar_proyectos'),
        #url(r'^modificar/(?P<id_proyecto>\d+)$', 'proyectos.views.editar_proyecto'),
        #url(r'^cambiarEstado/(?P<id_proyecto>\d+)$', 'proyectos.views.cambiar_estado_proyecto'),
        #url(r'^importar/(?P<id_proyecto>\d+)$', 'proyectos.views.importar_proyecto'),
        #url(r'^equipo/(?P<id_proyecto>\d+)$', 'proyectos.views.ver_equipo'),
        url(r'^register/success/$',RegisterSuccessView ,name='RegisterSuccessView'),
        url(r'^register/failed/(?P<id_proyecto>\d+)$',RegisterFailedView, name='RegistroFallo')
        )