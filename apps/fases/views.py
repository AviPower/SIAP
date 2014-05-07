# -*- encoding: utf-8 -*-

__author__ = 'marcel'
__text__ = 'Este modulo contiene funciones que permiten el control de las fases'

from django.contrib.auth.decorators import login_required, permission_required
from apps.fases.forms import FaseForm, CambiarEstadoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.fases.models import Fase
from apps.fases.models import Fase
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from SIAP import settings
from apps.tiposDeItem.models import TipoItem


@login_required
#@permission_required('proyectos')
def registrar_fase(request):
    """
    Vista para registrar una nueva fase dentro de proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/fases/register/success') si el rol líder fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """

    if request.method == 'POST':
        formulario = FaseForm(request.POST)

        if formulario.is_valid():
            if formulario.cleaned_data['fecha_ini']>formulario.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE, "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider=formulario.cleaned_data['lider']
                #asigna el rol lider al usuario seleccionado
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
                formulario.save()
                return HttpResponseRedirect('/fases/register/success')
    else:
        formulario = FaseForm()
    return render_to_response('fases/registrar_fases.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required
@permission_required('proyectos, fases')
def listar_fases(request):
    """
    vista para listar las fases del proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('fases/listar_fases.html', {'datos': fases}, context_instance=RequestContext(request))
    """

    fases = Fase.objects.all().exclude(estado='COMPL')


    return render_to_response('fases/listar_fases.html', {'datos': fases}, context_instance=RequestContext(request))


@login_required
@permission_required('proyectos, fases')
def editar_fase(request,id_fase):
    """
    Vista para editar un proyecto,o su líder o los miembros de su comité
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: HttpResponseRedirect('/proyectos/register/success/') cuando el formulario es validado correctamente o render_to_response('proyectos/editar_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    proyecto= Fase.objects.get(id=id_fase)
    nombre= Fase.nombre
    if request.method == 'POST':
        # formulario enviado
        fase_form = FaseForm(request.POST, instance=fase)
        if fase_form.is_valid():
            if fase_form.cleaned_data['fecha_ini']>fase_form.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE, "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider=fase_form.cleaned_data['lider']
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
            # formulario validado correctamente
                fase_form.save()
                return HttpResponseRedirect('/fases/register/success/')
    else:
        # formulario inicial
        fase_form = FaseForm(instance=proyecto)
    return render_to_response('fases/editar_fases.html', { 'fases': fase_form, 'nombre':nombre}, context_instance=RequestContext(request))

