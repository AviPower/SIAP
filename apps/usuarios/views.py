from django.views.generic import CreateView, TemplateView, ListView
from django.core.urlresolvers import reverse_lazy
from .models import Usuario

class RegistrarUsuario(CreateView):
    template_name = 'usuarios/registrarUsuario.html'
    model = Usuario
    success_url = reverse_lazy('reportar_user')

class ReportarUsuario(ListView):
    template_name = 'usuarios/reportarUsuario.html'
    model = Usuario
    context_object_name = 'usuarios'