from django.views.generic import CreateView, TemplateView, ListView
from django.core.urlresolvers import reverse_lazy
from apps.inicio.models import Perfiles



class Usuario(TemplateView):
    template_name = 'usuarios/admin.html'

class ListUser(TemplateView):
    template_name = 'usuarios/user/user.html'

class AddUser(TemplateView):
    template_name = 'usuarios/user/add.html'

class NewPass(TemplateView):
    template_name = 'usuarios/cambiar_pass.html'