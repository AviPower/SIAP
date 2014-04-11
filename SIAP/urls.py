from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    #INICIO
    url(r'^', include('apps.inicio.urls')),
    #USUARIOS
    url(r'^usuario/',include('apps.usuarios.urls')),

)
