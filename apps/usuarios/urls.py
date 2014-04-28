__author__ = 'alvarenga'
from django.conf.urls import patterns, include, url
from .views import list_usuario, edit_user, delete_user, search_form, search
urlpatterns = patterns('',
    url(r'^$', list_usuario, name='usuario'),
    url(r'^edit/(?P<pk>\d+)/$', edit_user, name='usuario_edit'),
    url(r'^delete/(?P<pk>\d+)/$', delete_user, name='usuario_delete'),
    url(r'^nuevo_pass/$','apps.usuarios.views.password_change',name='cambiar_pass_done'),
    url(r'^nuevo_pass/done/$', 'apps.usuarios.views.password_change_done', name='cambiar_pass_done'),
    url(r'^search_form/$', search_form,name='search_form'),
    url(r'^search/$', search, name='search'),


)