__author__ = 'alvarenga'
from django.conf.urls import patterns, include, url
from .views import RegistrarUsuario, ReportarUsuario
urlpatterns = patterns('',

    url(r'^registrar/$',RegistrarUsuario.as_view(),name='registro_user'),
    url(r'^reportar/$',ReportarUsuario.as_view(),name='reportar_user'),

)