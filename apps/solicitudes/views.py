# -*- encoding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import RequestContext
from SIAP import settings
from apps.items.models import Item
from apps.fases.models import Fase
from apps.items.views import getMaxIdItemEnLista, itemsProyecto, contar_solicitudes
from apps.proyectos.models import Proyecto
from apps.solicitudes.forms import VotoForm
from apps.solicitudes.models import Solicitud, Voto, ItemsARevision
from django.contrib.auth.decorators import login_required, permission_required
from apps.lineaBase.views import es_lider

__author__ = 'marcel'
__text__ = 'Este modulo contiene funciones que permiten el control de solicitudes de cambio'


@login_required
def listar_solicitudes(request):

    '''
    vista para listar las solicitudes de cambio de un usuario que pertenezca a algun
    comite de cambios
    '''

    request.session['cantSolicitudes']=contar_solicitudes(request.user.id)
    request.session['nivel'] = 0

    lista_proyectos=Proyecto.objects.filter(comite__id=request.user.id)
    lista_solicitudes=[]
    if len(lista_proyectos)==0:
        return HttpResponseRedirect('/denegado')

    for proyecto in lista_proyectos:
        lista=Solicitud.objects.filter(proyecto=proyecto,estado='PENDIENTE')
        for solicitud in lista:
            lista_solicitudes.append(solicitud)
    return render_to_response('solicitudes/listar_solicitudes.html', {'datos': lista_solicitudes}, context_instance=RequestContext(request))


def puede_votar(id_usuario,id_solicitud):
    '''
    funcion que sirve para determinar si un usuario puede o no votar,
    puede votar si:
    1) Pertenece al comite del proyecto
    2) Aun no ha votado antes
    '''
    solicitud=get_object_or_404(Solicitud, id=id_solicitud)
    lista_proyectos=Proyecto.objects.filter(comite__id=id_usuario, id=solicitud.proyecto.id)
    if len(lista_proyectos)==0:
        return HttpResponseRedirect('/denegado')
    voto=Voto.objects.filter(usuario_id=id_usuario, solicitud=solicitud)
    if len(voto)!=0:
        return False
    else:
        return True

@login_required
def votar(request, id_solicitud):
    '''
    vista en la cual un miembro del comite emite su voto
    Tambien se comprueba que con el voto la solicitud ya sea aprobada, rechazada o siga pendiente
    1) Si es aprobada el item pasa a CON y sus items relacionados a REV y la linea base a ROTA
    2) Si es rechazada el item pasa a FIN y la linea base queda en CERRADA
    3) Si sige pendiente el item continua BLO
    '''
    solicitud=get_object_or_404(Solicitud, id=id_solicitud)
    if puede_votar(request.user.id, id_solicitud)!=True:
        return HttpResponseRedirect('/denegado')
    item=solicitud.item
    if request.method=='POST':
        formulario=VotoForm(request.POST)
        if formulario.is_valid():
            voto=Voto(solicitud=solicitud,usuario=request.user,voto=request.POST['voto'])
            voto.save()
            votacionCerrada(solicitud)
            aprobada=2
            if votacionCerrada(solicitud):
                resultado(solicitud)
                if solicitud.estado=='APROBADA':
                    aprobada=1
                    item.estado='FIN'
                    item.save()
                    listaitems =itemsProyecto(solicitud.proyecto)
                    maxiditem = getMaxIdItemEnLista(listaitems)
                    global nodos_visitados
                    global papa
                    papa=item
                    nodos_visitados = [0]*(maxiditem+1)
                    estadoDependientes(item.id)
                    item.estado='CON'
                    item.save()
                    lb=item.lineaBase
                    lb.estado='ROTA'
                    lb.save()
                else:
                    item.estado='FIN'
                    item.save()
                    aprobada=0
            request.session['cantSolicitudes']=contar_solicitudes(request.user.id)
            return render_to_response('solicitudes/votacion_satisfactoria.html',{'aprobada':aprobada}, context_instance=RequestContext(request))
    else:
        formulario=VotoForm()
    return render_to_response('solicitudes/votar_solicitud.html',{'formulario':formulario,'solicitud':solicitud}, context_instance=RequestContext(request))

def estadoDependientes(id_item):
    '''
    Funcion para recorrer el grafo de items del proyecto en profundidad
    Pasando todos los items relacionados con id_item a REV
    '''
    global nodos_visitados
#    print id_item
    nodos_visitados[id_item]=1
    item=get_object_or_404(Item,id=id_item)
#    print item.estado
#    print(not(item.estado=='CON' or item.estado=='BLO' or item.estado=='PEN'))
    if not(item.estado=='CON' or item.estado=='BLO' or item.estado=='PEN' or item.estado=='ANU'):
        if item!=papa:
            revision=ItemsARevision(item_bloqueado=papa, item_revision=item)
            revision.save()
        item.estado='REV'
        item.save()
        relaciones = Item.objects.filter(relacion=item.id)
        for relacion in relaciones:
            if(nodos_visitados[relacion.id]==0):
                estadoDependientes(relacion.id)



def votacionCerrada(solicitud):
    '''
    FUncion que comprueba si ya todos los mimebros del comite emitieron su voto
    '''
    comite = User.objects.filter(comite__id=solicitud.proyecto.id)
    voto=[]
    for miembro in comite:
        voto=Voto.objects.filter(usuario_id=miembro.id, solicitud_id=solicitud.id)
        if len(voto)==0:
            return False
    return True


def detalle_solicitud(request,id_solicitud):
    '''
    Vista para ver los detalles de una solicitud, junto con la cantidad de miembros
    y votos que se emitieron
    '''
    solicitud=get_object_or_404(Solicitud, id=id_solicitud)
    id_usuario=request.user.id
    lista_proyectos=Proyecto.objects.filter(comite__id=id_usuario, id=solicitud.proyecto.id)
    if len(lista_proyectos)==0:
        return HttpResponseRedirect('/denegado')

    votos = Voto.objects.filter(solicitud_id=solicitud.id)
    favor=0
    contra=0
    usuarios=[]
    for voto in votos:
        usuarios.append(voto.usuario)
        if voto.voto=='RECHAZAR':
            contra+=1
        else:
            favor+=1
    return render_to_response('solicitudes/detalle_solicitud.html',{'usuarios':usuarios,'solicitud':solicitud, 'favor':favor, 'contra':contra}, context_instance=RequestContext(request))


def resultado(solicitud):
    '''
    Funcion que cuenta los votos emitidos y que detemrina si la solicitud es aprobada o
    rechazada
    1) Se manda un mail al usuario solicitante comunicandole el resultado y tambien cambia
    el estado de la solicitud
    '''
    votos = Voto.objects.filter(solicitud_id=solicitud.id)
    favor=0
    contra=0
    mail=solicitud.usuario.email
    proyecto=str(solicitud.proyecto.nombre)
    item=str(solicitud.item.nombre)
    usuario=str(solicitud.usuario.first_name)
    mail=str(solicitud.usuario.email)
    for voto in votos:
        if voto.voto=='RECHAZAR':
            contra+=1
        else:
            favor+=1

    if contra>favor:
        solicitud.estado='RECHAZADA'

        titulo='Solicitud de cambio Rechazada'
        mensaje=usuario + ', su solicitud de cambio para el item ' + item + ' del proyecto ' + proyecto + ' ha sido rechazada.'


    else:
        solicitud.estado='APROBADA'
        titulo='Solicitud de cambio Aprobada'
        mensaje=usuario + ', su solicitud de cambio para el item ' + item + ' del proyecto ' + proyecto + ' ha sido aprobada.'

    correo=EmailMessage(titulo, mensaje, to=[mail])
    correo.send()
    solicitud.save()

def comprobar_items_fase(id_fase):
    '''
    Funcion que recibe el id de una fase y retorna verdadero o falso si es que todos los items de la
    misma se encuentran en una linea base
    '''
    items=Item.objects.filter(tipo_item__fase=id_fase).exclude(estado='ANU')
    if len(items)==0:
         return False
    for item in items:
        if item.lineaBase is None or item.estado!='FIN':
            return False
    return True

@login_required
def finalizar_fase(request, id_fase):

    '''
    vista para finalizar una fase. Los criterios que se tienen en cuenta para finalizarla son:
    1) La fase anterior debe estar finalizada
    2) Todos los items de la fase deben estar en una linea base
    '''
    fase=get_object_or_404(Fase,id=id_fase)

    comprobar_fase=False
    if es_lider(request.user.id, fase.proyecto_id):
        if fase.orden==1 and comprobar_items_fase(id_fase):
            comprobar_fase=True
        elif fase.orden!=1:
            fase_anterior=get_object_or_404(Fase, proyecto=fase.proyecto, orden=fase.orden-1)
            if comprobar_items_fase(fase.id) and fase_anterior.estado=='FIN':
                comprobar_fase=True
        if comprobar_fase:
            fase.estado='FIN'
            fase.save()
            return render_to_response('solicitudes/finalizacion_correcta.html', {'fase':fase}, context_instance=RequestContext(request))
        else:
            return render_to_response('solicitudes/finalizacion_incorrecta.html', {'fase':fase}, context_instance=RequestContext(request))

    else:
        return render_to_response('403.html')


def finalizar_proyecto(request, id_proyecto):

    '''
    vista para finalizar un Proyecyo. Los criterios que se tienen en cuenta para finalizarlo son:
    1) Todas las fases deben estar finalizadas

    '''
    puede_finalizar=True
    if not es_lider(request.user.id, id_proyecto):
        return HttpResponseRedirect ('/denegado')
    proyecto=get_object_or_404(Proyecto,id=id_proyecto)
    fases=Fase.objects.filter(proyecto=proyecto)
    for fase in fases:
        if fase.estado!='FIN':
            puede_finalizar=False
            break
    if puede_finalizar:
        proyecto.estado='FIN'
        proyecto.save()
        return render_to_response('solicitudes/finalizacion_correcta_proyecto.html', {'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('solicitudes/finalizacion_incorrecta_proyecto.html', {'proyecto':proyecto}, context_instance=RequestContext(request))