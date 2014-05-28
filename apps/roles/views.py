__author__ = 'alvarenga'
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import Group, Permission
from django.http import HttpResponse, HttpResponseRedirect, request
from django.template import RequestContext
from django.views.generic import TemplateView
from apps.roles.forms import GroupForm
from django.shortcuts import render_to_response
from django.db.models import Q
from apps.fases.models import Fase
from apps.roles.models import Rol
from django.contrib import messages
from SIAP import settings

__text__ = 'Este modulo contiene funciones que permiten el control de roles'

@login_required
@permission_required('group')
def crear_rol(request):
    """
    vista para crear un rol, que consta de un nombre y una lista de permisos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: return HttpResponseRedirect('/roles/register/success/') o render_to_response('roles/crear_rol.html', { 'group_form': group_form}, context_instance=RequestContext(request))
    """
    if request.method == 'POST':
        # formulario enviado
        group_form = GroupForm(request.POST)

        if group_form.is_valid():
            # formulario validado correctamente
            group_form.save()
            return HttpResponseRedirect('/roles/register/success/')

    else:
        # formulario inicial
        group_form = GroupForm()
    return render_to_response('roles/crear_rol.html', { 'group_form': group_form}, context_instance=RequestContext(request))


@login_required
@permission_required('group')
def lista_roles(request):
    """
    vista para listar los roles existentes en el sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('roles/listar_roles.html', {'datos': grupos}, context_instance=RequestContext(request))
    """

    grupos = Group.objects.all()
    return render_to_response('roles/listar_roles.html', {'datos': grupos}, context_instance=RequestContext(request))

@login_required
@permission_required('group')
def buscarRol(request):
    """
    vista para buscar un rol entre todos los registrados en el sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: return render_to_response('roles/listar_roles.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__contains=query)
        )
        results = Group.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('roles/listar_roles.html', {'datos': results}, context_instance=RequestContext(request))


@login_required
@permission_required('group')
def detalle_rol(request, id_rol):
    """
    vista para ver los detalles del rol <id_rol> del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_rol: referencia a los roles
    @return: render_to_response('roles/detalle_rol.html', {'rol': dato, 'permisos': permisos}, context_instance=RequestContext(request))
    """

    dato = get_object_or_404(Group, pk=id_rol)
    permisos = Permission.objects.filter(group__id=id_rol)
    return render_to_response('roles/detalle_rol.html', {'rol': dato, 'permisos': permisos}, context_instance=RequestContext(request))

@login_required
@permission_required('group')
def eliminar_rol(request, id_rol):
    """
    vista para eliminar el rol <id_rol>. Se comprueba que dicho rol no tenga fases asociadas.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_rol: referencia a los roles
    @return: render_to_response('roles/listar_roles.html', {'datos': grupos}, context_instance=RequestContext(request))
    """

    dato = get_object_or_404(Group, pk=id_rol)
    fases=Fase.objects.filter(roles__id=dato.id)
    grupos = Group.objects.all()
    if dato.name=='Lider':
        return render_to_response('roles/listar_roles.html', {'datos': grupos, 'mensaje':0}, context_instance=RequestContext(request))
    else:
        if fases.count()==0:
            dato.delete()
            return render_to_response('roles/listar_roles.html', {'datos': grupos,'mensaje':1}, context_instance=RequestContext(request))
        else:
            return render_to_response('roles/listar_roles.html', {'datos': grupos,'mensaje':2}, context_instance=RequestContext(request))
    grupos = Group.objects.all()
    return render_to_response('roles/listar_roles.html', {'datos': grupos, 'mensaje':1000}, context_instance=RequestContext(request))


class RegisterSuccessView(TemplateView):
    template_name = 'roles/creacion_correcta.html'

@login_required
@permission_required('group')
def editar_rol(request,id_rol):
    """
    vista para cambiar el nombre del rol o su lista de permisos.
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_rol: referencia a los roles
    @return: HttpResponseRedirect('/roles/register/success/') o render_to_response('roles/editar_rol.html', { 'rol': rol_form, 'dato':rol}, context_instance=RequestContext(request))
    """
    rol= Group.objects.get(id=id_rol)
    if request.method == 'POST':
        # formulario enviado
        rol_form = GroupForm(request.POST, instance=rol)

        if rol_form.is_valid():
            # formulario validado correctamente
            rol_form.save()
            return HttpResponseRedirect('/roles/register/success/')

    else:
        # formulario inicial
        rol_form = GroupForm(instance=rol)
    return render_to_response('roles/editar_rol.html', { 'rol': rol_form, 'dato':rol}, context_instance=RequestContext(request))
