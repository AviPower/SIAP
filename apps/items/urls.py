from django.conf.urls import patterns, url
from django.contrib import admin
from apps.items.views import listar_proyectos,listar_fases,listar_tiposDeItem, crear_item, listar_items, detalle_item, crear_solicitud
from apps.items.views import editar_item, eliminar_archivo,detalle_tiposDeItem, seleccion_tipoItem, crear_item_hijo,cambiar_estado_item
from apps.items.views import listar_archivos, detalle_version_item, listar_versiones, reversionar_item,descargo_archivo, cambiar_padre,\
    cambiar_antecesor,grafo_relaciones
admin.autodiscover()


urlpatterns = patterns('',
        url(r'^proyectos/$',listar_proyectos, name='listar_proyectos'),
        url(r'^proyectos/fases/(?P<id_proyecto>\d+)$',listar_fases, name='listar_fases'),
        url(r'^fases/tiposDeItem/(?P<id_fase>\d+)$',listar_tiposDeItem, name='listar_tiposDeItem'),
        url(r'^fases/tiposDeItem/detalle/(?P<id_tipoItem>\d+)$',detalle_tiposDeItem, name='detalle_tiposDeItem'),
        url(r'^item/selectTipoItem/(?P<id_fase>\d+)$',seleccion_tipoItem, name='seleccion_tipoItem'),
        url(r'^item/crear/(?P<id_tipoItem>\d+)$',crear_item, name='crear_item'),
        url(r'^item/listar/(?P<id_fase>\d+)$',listar_items, name='listar_items'),
        url(r'^item/detalle/(?P<id_item>\d+)$',detalle_item, name='detalle_item'),
        url(r'^item/modificar/(?P<id_item>\d+)$',editar_item, name='editar_item'),

        url(r'^item/versiones/(?P<id_item>\d+)$',listar_versiones,name='listar_versiones'),
        url(r'^item/reversionar/(?P<id_version>\d+)$',reversionar_item,name='reversionar_item'),
        url(r'^item/archivos/(?P<id_item>\d+)$',listar_archivos, name='listar_archivos'),
        url(r'^item/descargar/(?P<idarchivo>\d+)$',descargo_archivo, name='descargar_archivos'),
        url(r'^item/archivos/eliminar/(?P<id_archivo>\d+)$',eliminar_archivo,name='eliminar_archivo'),
        url(r'^item/detalle/version/(?P<id_version>\d+)$',detalle_version_item, name='detalle_version'),
        url(r'^item/crear/hijo/(?P<id_item>\d+)$',crear_item_hijo,name='crear_hijo'),
        url(r'^item/cambiar_estado/(?P<id_item>\d+)$',cambiar_estado_item,name='cambiar_estado'),

        url(r'^item/padre/(?P<id_item>\d+)$',cambiar_padre,name='cambiar_padre'),
        url(r'^item/antecesor/(?P<id_item>\d+)$',cambiar_antecesor,name='cambiar_antecesor'),
        url(r'^item/grafo/(?P<id_fase>\d+)$',grafo_relaciones,name='grafo_relaciones'),
        url(r'^item/solicitud/(?P<id_item>\d+)$',crear_solicitud,name='crear_solicitud'),
        )