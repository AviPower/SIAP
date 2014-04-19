from django.views.generic import FormView, TemplateView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import  PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.shortcuts import resolve_url
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect



class Usuario(TemplateView):
    template_name = 'usuarios/admin.html'

class ListUser(TemplateView):
    template_name = 'usuarios/user/user.html'

class AddUser(TemplateView):
    template_name = 'usuarios/user/add.html'

class ListUserper(TemplateView):
    template_name = 'usuarios/user/userper.html'

class AddUserper(TemplateView):
    template_name = 'usuarios/user/addper.html'

@sensitive_post_parameters()
@csrf_protect
@login_required
def password_change(request,
                    template_name='usuarios/cambiar_pass.html',
                    post_change_redirect=None,
                    password_change_form=PasswordChangeForm,
                    current_app=None, extra_context=None):
    """
    Verifica que no halla ningun error al cambiar el password
    """
    if post_change_redirect is None:
        post_change_redirect = reverse('password_change_done')
    else:
        post_change_redirect = resolve_url(post_change_redirect)
    if request.method == "POST":
        form = password_change_form(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(post_change_redirect)
    else:
        form = password_change_form(user=request.user)
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)

@login_required
def password_change_done(request,
                         template_name='usuarios/user/cambiar_pass_done.html',
                         current_app=None, extra_context=None):
    """
    Redirecciona una vez siguiente pagina confirmando el cambio exitoso de password
    """
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)