from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from datetime import datetime
# Create your views here.
from django.template import RequestContext
from SIAP import settings
from apps.fases.models import Fase
from apps.items.models import Item, Archivo, AtributoItem, VersionItem
from apps.proyectos.models import Proyecto
from apps.tiposDeItem.models import TipoItem, Atributo
from apps.lineaBase.models import LineaBase
from apps.lineaBase.forms import LineaBaseForm
from apps.items.views import generar_version
from django import forms


def es_lider(id_usuario, id_proyecto):
    '''
    Funcion que devuelve si un usuario es o no el lider del proyecto especificado
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto dentro de la base de datos
    @return Boolean
    '''
    proyecto=get_object_or_404(Proyecto, id=id_proyecto)
    if proyecto.lider.id==id_usuario:
        return True
    else:
        return False

@login_required

def listar_lineasBase(request, id_fase):

    '''
    vista para listar las lineas base de una fase
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    fase=get_object_or_404(Fase,id=id_fase)
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    lineasbase=LineaBase.objects.filter(fase_id=id_fase)
    if es_lider(request.user.id, fase.proyecto_id)==False:
        return HttpResponseRedirect('/denegado')

    return render_to_response('lineaBase/listar_lineaBase.html', {'datos': lineasbase, 'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
def crear_lineaBase(request, id_fase):

    '''
    vista para crear una linea base.
    Una vez que se crea se asigna el id correspondiente a los items seleccionados, y
    se cambia el estado de los mismos a FIN
    y el estado de la linea base creada es CERRADA
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_fase: referencia a la fase dentro de la base de datos
    @return render_to_response
    '''

    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    fase=get_object_or_404(Fase,id=id_fase)
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    if es_lider(request.user.id, fase.proyecto_id)==False:
        return HttpResponseRedirect('/denegado')
    if fase.estado=='FIN':
        return HttpResponse('<h1>No se pueden crear lineas base ya que la fase ha finalizado</h1>')
    items=[]
    titem=TipoItem.objects.filter(fase_id=fase.id)
    for i in titem:
        it=Item.objects.filter(tipo_item_id=i.id, estado='VAL', lineaBase=None)
        for ii in it:
            items.append(ii)
    if len(items)==0:
        return HttpResponse('<h1>No se pueden crear lineas base ya que aun no existen items con estado validado</h1>')

    if request.method=='POST':

                formulario = LineaBaseForm(fase,request.POST)
                items=request.POST.get('items')
                if items is None:
                    pass

                else:
                    if request.POST['nombre']=='':
                        pass
                    else:
                        items= request.POST.getlist('items')

                        flag=False
                        nombre=''
                        for item in items:
                            i=Item.objects.get(id=item)
                            if i.relacion!=None:
                                if i.relacion.estado!='FIN':
                                    flag=True
                                    nombre=i.nombre
                        if flag==True:
                            return render_to_response('lineaBase/generar_lineaBase.html', {'formulario':formulario,'items':items,'mensaje':0,'men':'El item ' + str(nombre)+ ' posee una relacion con un item no Finalizado' ,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
                            messages.add_message(request,settings.DELETE_MESSAGE,'El item ' + str(nombre)+ ' posee una relacion con un item no Finalizado')
                        else:
                            cod=lineabase=LineaBase(nombre=request.POST['nombre'], fase=fase, estado='C')
                            lineabase.save()
                            items= request.POST.getlist('items')
                            for item in items:
                                i=Item.objects.get(id=item)
                                generar_version(i)
                            for item in items:
                                i=Item.objects.get(id=item)
                                i.estado='FIN'
                                i.lineaBase=cod
                                i.save()
                            return render_to_response('lineaBase/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))

    else:
        formulario=LineaBaseForm(fase=fase)
        items=Item.objects.filter(estado='VAL', tipo_item__fase=fase.id, lineaBase=None)
    return render_to_response('lineaBase/generar_lineaBase.html', {'formulario':formulario,'items':items, 'mensaje':1000,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
def detalle_lineabase(request, id_lb):

    '''
    vista para ver los detalles de la linea base especificada junto con sus items asosciados
    '''
    lineabase=get_object_or_404(LineaBase,id=id_lb)

    fase=lineabase.fase
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    if es_lider(request.user.id, fase.proyecto_id):
        items=Item.objects.filter(lineaBase=lineabase)
        dato=lineabase
        return render_to_response('lineaBase/detalle_lineaBase.html', {'datos': dato, 'items':items, 'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')