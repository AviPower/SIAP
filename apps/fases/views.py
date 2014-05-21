# -*- encoding: utf-8 -*-

__text__ = 'Este modulo contiene funciones que permiten el control de las fases'

from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
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
    mensaje=100
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #Comprobacion de formato de fecha
                mensaje=0
                return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':mensaje,'id':id_proyecto}, context_instance=RequestContext(request))
            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha,estado = "PEN", proyecto_id = id_proyecto)
                aux=0
                orden=Fase.objects.filter(proyecto_id=id_proyecto)

                if aux>0:#comprobacion de pertenencia de roles
                    aux=1
                else:
                    proyecto=Proyecto.objects.get(id=id_proyecto)
                    cantidad = orden.count()
                    if cantidad>0:#comprobaciones de fecha
                       anterior = Fase.objects.get(orden=cantidad, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                           #Fecha de inicio no concuerda con fase anterior
                           return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':1,'id':id_proyecto,'proyecto':proyecto}, context_instance=RequestContext(request))
                       else:
                            if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                #Fecha de inicio no concuerda con proyecto
                                print(fecha1)
                                print(datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d'))
                                print (datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d'))
                                return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':2,'id':id_proyecto,'proyecto':proyecto}, context_instance=RequestContext(request))
                            else:
                                newFase.orden=orden.count()+1 #Calculo del orden de la fase a crear
                                newFase.save()
                                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                        newFase.orden=1
                        newFase.save()
                        return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFaseForm() #formulario inicial
    return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'id':id_proyecto, 'proyecto':proyecto, 'mensaje':mensaje}, context_instance=RequestContext(request))



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
        return render_to_response('fases/error_activo.html',{'datos': fases, 'proyecto' : id_proyecto}, context_instance=RequestContext(request))
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
        mensaje =100
        fase_form = ModificarFaseForm(request.POST, instance=fase)
        if fase_form.is_valid():
            if len(str(request.POST["fInicio"])) != 10 : #comprobacion de formato de fecha
                mensaje=0
                return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
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
                            mensaje=1
                            return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                       else:
                           if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                               mensaje=2
                               return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                           else:
                                if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                    mensaje=3
                                    return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                                else:
                                    fase_form.save()
                                    return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and fase.orden != cantidad and fase.orden==1:
                   siguiente = Fase.objects.get(orden=(fase.orden)+1, proyecto_id=id_proyecto)
                   if fecha1>datetime.strptime(str(siguiente.fInicio),'%Y-%m-%d'):
                        mensaje=2
                        return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                   else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            mensaje=3
                            return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                        else:
                            fase_form.save()

                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                elif cantidad>1 and fase.orden == cantidad:
                    anterior = Fase.objects.get(orden=(fase.orden)-1, proyecto_id=id_proyecto)
                    if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                        mensaje=1
                        return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                        if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                            mensaje=3
                            return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                        else:
                            fase_form.save()
                            return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                else:
                    if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                        mensaje=3
                        return render_to_response('fases/editar_fase.html', { 'form': fase_form,'mensaje':mensaje, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                        fase_form.save()
                        return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        # formulario inicial
        fase_form = ModificarFaseForm(instance=fase)
    return render_to_response('fases/editar_fase.html', { 'form': fase_form, 'fase': fase, 'id_proyecto':id_proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('fase')
def fases_todas(request,id_proyecto):
    '''
    vista para listar las fases del sistema
    '''
    fases = Fase.objects.all()
    proyecto = Proyecto.objects.get(id=id_proyecto)
    return render_to_response('fases/fases_todas.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('fase')
def importar_fase(request, id_fase,id_proyecto):

    '''
        Vista para importar los datos de una fase existente para su utilizacion en la creacion de una nueva.
        Realiza las comprobaciones necesarias con respecto a la fecha de inicio y orden de fase.
    '''

    fase= Fase.objects.get(id=id_fase)
    if request.method=='POST':
        proyecto = Proyecto.objects.get(id=id_proyecto)
        formulario = CrearFaseForm(request.POST)
        if formulario.is_valid():
            if len(str(request.POST["fInicio"])) != 10 :
                mensaje=0
                return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':mensaje,'id':id_proyecto}, context_instance=RequestContext(request))

            else:
                fecha=datetime.strptime(str(request.POST["fInicio"]),'%d/%m/%Y')
                fecha=fecha.strftime('%Y-%m-%d')
                fecha1=datetime.strptime(fecha,'%Y-%m-%d')
                newFase = Fase(nombre = request.POST["nombre"],descripcion = request.POST["descripcion"],maxItems = request.POST["maxItems"],fInicio = fecha, estado = "PEN", proyecto_id = id_proyecto)
                aux=0
                orden=Fase.objects.filter(proyecto_id=id_proyecto)
                if aux>0:
                    messages.add_message(request, settings.DELETE_MESSAGE, "Error: No hacemos nada")
                else:
                    proyecto=Proyecto.objects.get(id=id_proyecto)
                    cantidad = orden.count()
                    if cantidad>0:
                       anterior = Fase.objects.get(orden=cantidad, proyecto_id=id_proyecto)
                       if fecha1<datetime.strptime(str(anterior.fInicio),'%Y-%m-%d'):
                            mensaje=1
                            return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':mensaje,'id':id_proyecto}, context_instance=RequestContext(request))

                       else:
                            if datetime.strptime(str(proyecto.fecha_ini),'%Y-%m-%d')>=fecha1 or datetime.strptime(str(proyecto.fecha_fin),'%Y-%m-%d')<=fecha1:
                                mensaje=2
                                return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':mensaje,'id':id_proyecto}, context_instance=RequestContext(request))

                            else:

                                newFase.orden=orden.count()+1
                                newFase.save()

                                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
                    else:
                                newFase.orden=1
                                newFase.save()
                                return render_to_response('fases/creacion_correcta.html',{'id_proyecto':id_proyecto}, context_instance=RequestContext(request))
    else:
        formulario = CrearFaseForm(initial={'descripcion':fase.descripcion, 'maxItems':fase.maxItems, 'fInicio':fase.fInicio, 'orden':fase.orden}) #'fInicio':datetime.strptime(str(fase.fInicio),'%Y-%m-%d').strftime('%d/%m/%y')
    return render_to_response('fases/registrar_fases.html',{'formulario':formulario,'mensaje':1000,'id':id_proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('fase')
def detalle_fase(request, id_fase):

    '''
    vista para ver los detalles del usuario <id_user> del sistema
    '''

    dato = get_object_or_404(Fase, pk=id_fase)
    proyecto = Proyecto.objects.get(id=dato.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html',{'proyecto':dato}, context_instance=RequestContext(request))
    return render_to_response('fases/detalle_fase.html', {'datos': dato,'proyecto_id':dato.proyecto_id}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def eliminar_fase(request,id_fase):
    '''
    vista que elimina una fase
    '''
    fase = get_object_or_404(Fase, pk=id_fase)
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado =='PEN':
        fase.delete()
    fases = Fase.objects.filter(proyecto_id=proyecto.id).order_by('orden')
    return render_to_response('fases/listar_fases.html', {'datos': fases, 'proyecto' : proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('fase')
def buscar_fases(request,id_proyecto):
    """
    vista para buscar las fases del proyecto
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if query:
        qset = (
            Q(nombre__contains=query)
        )
        results = Fase.objects.filter(qset, proyecto_id=id_proyecto).distinct()
    else:
        results = []


    return render_to_response('fases/listar_fases.html', {'datos': results, 'proyecto' : proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def asignar_usuario(request,id_fase):
    '''
    vista auxiliar para obtener un listado de usuarios para asociar a la fase
    '''

    usuarios=User.objects.filter(is_active=True)
    fase=Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    return render_to_response('fases/lista_usuarios.html', {'datos': usuarios, 'fase' : fase,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def asignar_rol(request,id_usuario, id_fase):
    '''
    vista auxiliar para obtener el listado de roles asociados a una fase para asociarlos a un usuario
    '''
    fase=Fase.objects.get(id=id_fase)
    usuario=User.objects.get(id=id_usuario)
    roles=Group.objects.filter(fase__id=id_fase)
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    return render_to_response('fases/listar_roles.html', {'roles': roles, 'usuario':usuario, 'fase':id_fase,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required
@permission_required('fase')
def asociar(request,id_rol,id_usuario,id_fase):
    '''
    vista para asociar un rol perteneciente a una face a un usuario, asociandolo de esta manera a la fase, y al proyecto
    '''
    fase=Fase.objects.get(id=id_fase)
    usuario=User.objects.get(id=id_usuario)
    rol = Group.objects.get(id=id_rol)
    usuario.groups.add(rol)
    usuario.save()
    return HttpResponseRedirect('/fases/proyecto/'+str(fase.proyecto_id))


@login_required
@permission_required('fase')
def des(request,id_fase):
    '''
    vista para listar a los usuario de una fase, para poder desasociarlos
    '''
    fase=Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    roles=Group.objects.filter(fase__id=id_fase)
    usuarios=[]
    for rol in roles:
        p=User.objects.filter(groups__id=rol.id)
        for pp in p:
            usuarios.append(pp)
    return render_to_response('fases/desasignar_usuarios.html', {'datos': usuarios,'fase':id_fase,'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('fase')
def desasociar(request,id_usuario, id_fase):
    '''
    vista para remover un rol al usuario, desasociandolo asi de una fase
    '''
    fase=Fase.objects.get(id=id_fase)
    proyecto = Proyecto.objects.get(id=fase.proyecto_id)
    if proyecto.estado!='PEN':
        return render_to_response('fases/error_activo.html')
    usuario=User.objects.get(id=id_usuario)
    roles=Group.objects.filter(fase__id=id_fase)
    for rol in roles:
        usuario.groups.remove(rol)
        usuario.save()

    return HttpResponseRedirect('/fases/proyecto/'+str(fase.proyecto_id))

