__author__ = 'alvarenga'
from django.conf.urls import patterns, url
from django.contrib import admin
admin.autodiscover()
from apps.reportes.views import listar_proyectos_reporte, descargar_reporteProyectoLider,descargar_reporteItems, descargar_reporteVersionesItems, descargar_reporteSolicitudes, descargar_reporteLB, descargar_reporteUsuarios, descargar_reporteRoles,descargar_reporteProyectos

urlpatterns = patterns('',
    url(r'^listar_proyectos_reporte/$',listar_proyectos_reporte,name='listar_proyectos_reporte'),
    url(r'^proyecto/proyecto/(?P<id_proyecto>\d+)$',descargar_reporteProyectoLider,name='descargar_reporteProyectoLider'),
    url(r'^proyecto/items/(?P<id_proyecto>\d+)$',descargar_reporteItems,name='descargar_reporteItems'),
    url(r'^proyecto/versionesItems/(?P<id_proyecto>\d+)$',descargar_reporteVersionesItems,name='descargar_reporteVersionesItems'),
    url(r'^proyecto/solicitudesCambio/(?P<id_proyecto>\d+)$',descargar_reporteSolicitudes,name='descargar_reporteSolicitudes'),
    url(r'^proyecto/lineasBase/(?P<id_proyecto>\d+)$',descargar_reporteLB,name='descargar_reporteLB'),
    url(r'^usuarios/$',descargar_reporteUsuarios,name='descargar_reporteUsuarios'),
    url(r'^roles/$',descargar_reporteRoles,name='descargar_reporteRoles'),
    url(r'^proyectos/$',descargar_reporteProyectos,name='descargar_reporteProyectos'),

    url(r'^ReportesProyectos/$',descargar_reporteProyectos,name='descargar_reporteProyectos'),
)