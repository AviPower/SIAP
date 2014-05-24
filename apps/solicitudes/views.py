# -*- encoding: utf-8 -*-

from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from datetime import datetime
from apps.solicitudes.forms import SolicitudForm, CambiarEstadoForm#, VotoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.solicitudes.models import Solicitud, Voto
from apps.fases.models import Fase
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from SIAP import settings
from apps.tiposDeItem.models import TipoItem

__author__ = 'marcel'
__text__ = 'Este modulo contiene funciones que permiten el control de solicitudes de cambio'



@login_required
@permission_required('fases')
def registrar_solicitud(request):
    """
    vista para crear un rol, que consta de un nombre y una lista de permisos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: return HttpResponseRedirect('/roles/register/success/') o render_to_response('roles/crear_rol.html', { 'group_form': group_form}, context_instance=RequestContext(request))
    """
    if request.method == 'POST':
        # formulario enviado
        solicitud_form = SolicitudForm(request.POST)

        if solicitud_form.is_valid():
            # formulario validado correctamente
            solicitud_form.save()
            return HttpResponseRedirect('/solicitudes/register/success/')

    else:
        # formulario inicial
        solicitud_form = SolicitudForm()
    return render_to_response('solicitudes/crear_solicitud.html', { 'solicitud_form': solicitud_form}, context_instance=RequestContext(request))


@login_required
@permission_required('fases')
def listar_solicitudes(request):
    """
    vista para listar los roles existentes en el sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('roles/asignar_rol.html', {'datos': grupos}, context_instance=RequestContext(request))
    """

    solicitudes = Solicitud.objects.all()
    return render_to_response('solicitudes/listar_solicitudes.html', {'datos': solicitudes}, context_instance=RequestContext(request))

@login_required
@permission_required('fases')
def buscar_solicitud(request):
    """
    vista para buscar un rol entre todos los registrados en el sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: return render_to_response('roles/asignar_rol.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(name__contains=query)
        )
        results = Solicitud.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response('solicitudes/listar_solicitudes.html', {'datos': results}, context_instance=RequestContext(request))


@login_required
@permission_required('fases')
def detalle_solicitud(request, id_solicitud):
    """
    vista para ver los detalles del rol <id_rol> del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_rol: referencia a los roles
    @return: render_to_response('roles/detalle_rol.html', {'rol': dato, 'permisos': permisos}, context_instance=RequestContext(request))
    """

    dato = get_object_or_404(Solicitud, pk=id_solicitud)
    votos = Voto.objects.filter(solicitud__id=id_solicitud)
    return render_to_response('solicitudes/detalle_solicitudes.html', {'solicitud': dato, 'votos': votos}, context_instance=RequestContext(request))

@login_required
@permission_required('fases')
def RegisterSuccessView(request):
    """
    Vista llamada en caso de creación correcta de un proyecto, redirige a un template de éxito
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/creacion_correcta.html', context_instance=RequestContext(request))
    """
    return render_to_response('solicitudes/creacion_correcta.html', context_instance=RequestContext(request))


@login_required
@permission_required('fases')
def RegisterFailedView(request, id_fase):
    """
    Vista que retorna a un template de fracaso en caso de que el proyectos no pueda cambiar de estado
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto}, context_instance=RequestContext(request))
    """
    return render_to_response('solicitudes/cambio_estado_fallido.html', {'dato': id_fase},
                              context_instance=RequestContext(request))
