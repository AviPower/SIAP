from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),

    #INICIO
    url(r'^', include('apps.inicio.urls')),
    #USUARIOS
    url(r'^usuario/',include('apps.usuarios.urls')),
    #PROYECTOS
    url(r'^proyectos/',include('apps.proyectos.urls')),
    #ROLES
    url(r'^roles/',include('apps.roles.urls')),
    #FASES
    url(r'^fases/', include('apps.fases.urls')),
    #TIPO DE ITEM
    url(r'^tiposDeItem/', include('apps.tiposDeItem.urls')),
    #Administracion Desarrollo items Proyectos en ejecucion
    url(r'^desarrollo/',include('apps.items.urls')),
    url(r'^denegado/$',TemplateView.as_view(template_name='403.html')),
    #Administracion de Linea Base
    url(r'^lineaBase/',include('apps.lineaBase.urls')),
    #SOLICITUDES DE CAMBIO
    url(r'^solicitudes/',include('apps.solicitudes.urls')),
    #REPORTES
    url(r'^reportes/',include('apps.reportes.urls')),
)
