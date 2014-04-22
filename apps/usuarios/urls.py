__author__ = 'alvarenga'
from django.conf.urls import patterns, include, url
from .views import Usuario, ListUser, AddUser, ListUserper, AddUserper, password_change
urlpatterns = patterns('',
    url(r'^$', Usuario.as_view(),name='usuario'),
    url(r'^add/$', AddUser.as_view(),name='usuario_add'),
    url(r'^user/$', ListUser.as_view(),name='usuario_user'),
    url(r'^nuevo_pass/$','apps.usuarios.views.password_change'),
    url(r'^nuevo_pass/done/$', 'apps.usuarios.views.password_change_done', name='password_change_done'),
    url(r'^addper/$', AddUserper.as_view(),name='usuario_addper'),
    url(r'^userper/$', ListUserper.as_view(),name='usuario_userper'),


)