__author__ = 'alvarenga'
from django.conf.urls import patterns, include, url
from .views import Usuario, ListUser, AddUser, NewPass, RegistrarUsuario, ReportarUsuario
urlpatterns = patterns('',
    url(r'^$', Usuario.as_view(),name='usuario'),
    url(r'^add/$', AddUser.as_view(),name='usuario_add'),
    url(r'^user/$', ListUser.as_view(),name='usuario_user'),
    url(r'^nuevo_pass/$', NewPass.as_view(),name='usuario_pass'),


)