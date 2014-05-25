__author__ = 'alvarenga'

from django.conf.urls import patterns, include, url
from .views import Registrarse,SIAP

urlpatterns = patterns('',

    url(r'^$','django.contrib.auth.views.login',
        {'template_name':'inicio/index.html'},name='login'),

    url(r'^cerrar/$','django.contrib.auth.views.logout_then_login',
        name='logout'),

    url(r'^registrarse/$',Registrarse.as_view(),name='registrarse'),

    url(r'^siap/$',SIAP.as_view(),name='siap'),


)