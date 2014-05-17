from django.conf.urls import patterns, url
from django.contrib import admin
from apps.items.views import listar_proyectos,listar_fases,listar_tiposDeItem, crear_item, listar_items, detalle_item
from apps.items.views import editar_item, eliminar_archivo
from apps.items.views import listar_archivos, detalle_version_item, listar_versiones, reversionar_item
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^proyectos/$',listar_proyectos, name='listar_proyectos'),
        url(r'^proyectos/fases/(?P<id_proyecto>\d+)$',listar_fases, name='listar_fases'),
        url(r'^fases/tiposDeItem/(?P<id_fase>\d+)$',listar_tiposDeItem, name='listar_tiposDeItem'),
        url(r'^item/crear/(?P<id_tipoItem>\d+)$',crear_item, name='crear_item'),
        url(r'^item/listar/(?P<id_tipo_item>\d+)$',listar_items, name='listar_items'),
        url(r'^item/detalle/(?P<id_item>\d+)$',detalle_item, name='detalle_item'),
        url(r'^item/modificar/(?P<id_item>\d+)$',editar_item, name='editar_item'),
        url(r'^item/versiones/(?P<id_item>\d+)$',listar_versiones,name='listar_versiones'),
        url(r'^item/reversionar/(?P<id_version>\d+)$',reversionar_item,name='reversionar_item'),
        url(r'^item/archivos/(?P<id_item>\d+)$',listar_archivos, name='listar_archivos'),
        url(r'^item/archivos/eliminar/(?P<id_archivo>\d+)$',eliminar_archivo,name='eliminar_archivo'),
        url(r'^item/detalle/version/(?P<id_version>\d+)$',detalle_version_item, name='detalle_version'),
        )