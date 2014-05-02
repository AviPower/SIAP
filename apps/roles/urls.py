__author__ = 'alvarenga'
from django.conf.urls import patterns, url, include
from django.contrib import admin
admin.autodiscover()

from .views import crear_rol, lista_roles, detalle_rol, eliminar_rol, editar_rol, buscarRol, RegisterSuccessView, buscarPermisos

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^crear/$', crear_rol, name='crear_rol'),
    url(r'^$',lista_roles,name='lista_roles'),
    url(r'^(?P<id_rol>\d+)$', detalle_rol, name='detalle_rol'),
    url(r'^eliminar/(?P<id_rol>\d+)$', eliminar_rol, name='eliminar_rol'),
    url(r'^modificar/(?P<id_rol>\d+)$', editar_rol, name='editar_rol'),
    url(r'^search/$',buscarRol, name='buscar_roles'),
    url(r'^searchpermisos/$',buscarPermisos, name='buscar_permisos'),
    url(r'^register/success/$',RegisterSuccessView.as_view()),
    )
