from django.views.generic import FormView
from .forms import UserForm
from django.core.urlresolvers import reverse_lazy
from .models import Perfiles


class Registrarse(FormView):
    """
    Recibe un @ctype  {FormView} y asigna un template para la operacion
    @c param FormView
    """
    template_name = 'inicio/registrarse.html'
    form_class = UserForm
    success_url = reverse_lazy('registrarse')

    def form_valid(self, form):
        """
        Formulario que valida los datos de usuario y perfil. Luego limpia los datos para comprobacion
        @param self: referencia al objeto
        @param form: Formulario de validacion del usuario
        """
        user = form.save()
        perfil = Perfiles()
        perfil.usuario = user
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        perfil.telefono = form.cleaned_data['telefono']
        perfil.direccion = form.cleaned_data['direccion']
        perfil.lider = False
        user.is_active = False
        user.is_staff = False
        user.save()
        perfil.save()
        return super(Registrarse,self).form_valid(form)

class SIAP(FormView):
    template_name = 'inicio/siap.html'
    form_class = UserForm
    success_url = reverse_lazy('siap')