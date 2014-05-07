# -*- encoding: utf-8 -*-

__author__ = 'marcel'
__text__ = 'Este modulo contiene funciones que permiten el control de las fases'

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.fases.models import Fase
from apps.fases.models import Fase
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from SIAP import settings
from django.contrib import messages
from django.shortcuts import render
from apps.proyectos.models import Proyecto
from apps.fases.forms import FaseForm, ModificarFaseForm, CrearFaseForm
from datetime import datetime


@login_required
@permission_required('fase')
def registrar_fase(request, id_proyecto):
    """
    Vista para registrar una nueva fase dentro de proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/fases/register/success') si el rol líder fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #Comprobacion de formato de fecha
                messages.add_message(request, settings.DELETE_MESSAGE, "Error: El formato de Fecha es: DD/MM/AAAA")
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha,estado = "PEN", proyecto_id = id_proyecto)
                aux=0
                orden=Fase.objects.filter(proyecto_id=id_proyecto)
                roles = request.POST.getlist("roles")
                for rol in roles:
                   fase=Fase.objects.filter(roles__id=rol)
                   if(fase.count()>0):
                     aux=1
                if aux>0:#comprobacion de pertenencia de roles
                    messages.add_message(request, settings.DELETE_MESSAGE, "Error: El Rol ya ha sido asignado a otra fase")
                else:
                    proyecto=Proyecto.objects.get(id=id_proyecto)
                    cantidad = orden.count()
                    if cantidad>0:#comprobaciones de fecha
                       anterior = Fase.objects.get(orden=cantidad, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                       else:
                            if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                            else:
                                roles = request.POST.getlist("roles")
                                newFase.orden=orden.count()+1 #Calculo del orden de la fase a crear
                                newFase.save()
                                for rol in roles:
                                    newFase.roles.add(rol)
                                    newFase.save()
                                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                        roles = request.POST.getlist("roles")
                        newFase.orden=1
                        newFase.save()
                        for rol in roles:
                            newFase.roles.add(rol)
                            newFase.save()
                        return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFaseForm()
    return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'id':id_proyecto},context_instance=RequestContext(request))


@login_required
@permission_required('proyectos, fases')
def listar_fases(request,id_proyecto):
    """
    vista para listar las fases del proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('fases/listar_fases.html', {'datos': fases}, context_instance=RequestContext(request))
    """
    fases = Fase.objects.filter(proyecto_id=id_proyecto).order_by('orden')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    else:
        return render_to_response('fases/listar_fases.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('proyectos, fases')
def editar_fase(request,id_fase):
    """
    Vista para editar un proyecto,o su líder o los miembros de su comité
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: HttpResponseRedirect('/proyectos/register/success/') cuando el formulario es validado correctamente o render_to_response('proyectos/editar_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    fase= Fase.objects.get(id=id_fase)
    id_proyecto= fase.proyecto_id
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    if request.method == 'POST':
        # formulario enviado
        fase_form = ModificarFaseForm(request.POST, instance=fase)

        if fase_form.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #comprobacion de formato de fecha
                messages.add_message(request, settings.DELETE_MESSAGE, "Error: El formato de Fecha es: DD/MM/AAAA")
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                proyecto=Proyecto.objects.get(id=fase.proyecto_id)
                orden=Fase.objects.filter(proyecto_id=proyecto.id)
                cantidad = orden.count()
                if cantidad>1 and fase.orden != cantidad and fase.orden >1: #comprobaciones de fechas
                       anterior = Fase.objects.get(orden=(fase.orden)-1, proyecto_id=id_proyecto)
                       siguiente = Fase.objects.get(orden=(fase.orden)+1, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                       else:
                           if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase siguiente")
                           else:
                                if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                    messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                                else:
                                    fase_form.save()
                                    return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and fase.orden != cantidad and fase.orden==1:
                   siguiente = Fase.objects.get(orden=(fase.orden)+1, proyecto_id=id_proyecto)
                   if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase siguiente")
                   else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                        else:
                            fase_form.save()
                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and fase.orden == cantidad:
                    anterior = Fase.objects.get(orden=(fase.orden)-1, proyecto_id=id_proyecto)
                    if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con fase anterior")
                    else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                        else:
                            fase_form.save()
                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                else:
                    if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                        messages.add_message(request, settings.DELETE_MESSAGE, "Error: Fecha de inicio no concuerda con proyecto")
                    else:
                        fase_form.save()
                        return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        fase_form = ModificarFaseForm(instance=fase)
    return render_to_response('fases/editar_fase.html', { 'form': fase_form, 'fase': fase}, context_instance=RequestContext(request))

