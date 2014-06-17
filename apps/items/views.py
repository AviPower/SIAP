from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission
from django.db.models import Q
from django.forms.models import modelformset_factory
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404
from datetime import datetime
# Create your views here.
import pydot
from django.template import RequestContext
from django.core.urlresolvers import reverse_lazy
from SIAP import settings
from apps.fases.models import Fase
from apps.items.models import Item, Archivo, AtributoItem, VersionItem
from apps.proyectos.models import Proyecto
from apps.tiposDeItem.models import TipoItem, Atributo
from apps.items.forms import EstadoItemForm, PrimeraFaseForm, SolicitudCambioForm
from apps.solicitudes.models import Solicitud,Voto
from django import forms

def contar_solicitudes(id_usuario):
    lista_proyectos=Proyecto.objects.filter(comite__id=id_usuario)
    lista_solicitudes=[]
    if len(lista_proyectos)==0:
        return 0;

    for proyecto in lista_proyectos:
        lista=Solicitud.objects.filter(proyecto=proyecto,estado='PENDIENTE')
        for solicitud in lista:
            votos=Voto.objects.filter(solicitud_id=solicitud.id, usuario_id=id_usuario)
            if(len(votos)==0):
                lista_solicitudes.append(solicitud)
    return len(lista_solicitudes)

def itemsProyecto(proyecto):
    '''
    Funcion que recibe como parametro un proyecto y retorna todos los items del mismo
    '''
    fases = Fase.objects.filter(proyecto_id=proyecto)
    items=[]
    for fase in fases:
        titem=TipoItem.objects.filter(fase=fase)
        for t in titem:
            item=Item.objects.filter(tipo_item=t)
            for i in item:
                if i.estado!='ANU':
                    items.append(i)
    return items


@login_required
def listar_proyectos(request):
    """
    vista para listar los proyectos asignados a un usuario expecifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return render_to_response('items/ingresar_proyecto.html', {'datos': setproyectos}, context_instance=RequestContext(request))
    """
    success_url = reverse_lazy('listar_proyectos')
    usuario = request.user
    #proyectos del cual es lider y su estado es activo
    proyectosLider = Proyecto.objects.filter(lider_id=usuario.id, estado='ACT')

    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    fases=[]
    proyectos=[]
    #las fases de en las cuales el usuario tiene un rol

    for rol in roles:
        print(rol.id)
        fase=Fase.objects.get(roles=rol.id)
        fases.append(fase)
    #los proyectos a los que pertenecen esas fases
    for fase in fases:
        proyecto=Proyecto.objects.get(id=fase.proyecto_id)
        if proyecto.estado=='ACT':
            proyectos.append(proyecto)
    for p in proyectosLider:
        proyectos.append(p)
    setproyectos=set(proyectos)
    return render_to_response('items/ingresar_proyecto.html', {'datos': setproyectos}, context_instance=RequestContext(request))

@login_required
def listar_fases(request, id_proyecto):
    """
    vista para listar las fases asignadas a un usuario de un proyecto especifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: clave foranea al proyecto
    @return: render_to_response(...)
    """
    #busca todas las fases del proyecto
    fasesProyecto=Fase.objects.filter(proyecto_id=id_proyecto, estado='EJE').order_by('orden')
    usuario = request.user
    proyecto=get_object_or_404(Proyecto,id=id_proyecto)
    fases=[]
    #si es lider pertenece a todas las fases
    if usuario.id==proyecto.lider_id:
        fases=fasesProyecto
    #si no, busca todas las fases en las que tiene algun rol asignado
    else:
        roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
        for rol in roles:
            for f in fasesProyecto:
                ff=Fase.objects.filter(id=f.id,roles__id=rol.id)
                for fff in ff:
                    fases.append(fff)
    #si no encuentra ninguna fase, significa que alguien que no tiene permisos esta tratando de ver
    #fases que no le correponden, se redirige al template de prohibido
    if len(fases)==0:
        return render_to_response('403.html')
    nivel = 1
    return render_to_response('items/ingresar_fase.html', {'datos': fases, 'nivel':nivel, 'proyecto':proyecto}, context_instance=RequestContext(request))

def es_miembro(id_usuario, id_fase,permiso):
    """
    funcion que recibe el id de un usuario y de una fase y devuelve true si el usuario tiene alguna fase asignada
    o false si no tiene ningun rol en esa fase
    Ademas verifica que el estado de la fase se EJE
    @param id_usuario: clave foranea al usuario
    @param id_fase: clave foranea a la fase
    @return booelean
    """

    fase=get_object_or_404(Fase,id=id_fase) #busca la fase
    usuario=User.objects.get(id=id_usuario) #busca el usuario
    proyecto=get_object_or_404(Proyecto,id=fase.proyecto_id) #el proyecto
    if fase.estado!='EJE':
        return False
    if usuario.id==proyecto.lider_id:
        return True
    rol_usuario=None
    roles=Group.objects.filter(user__id=usuario.id).exclude(name='Lider')
    roles_fase=Group.objects.filter(fase__id=fase.id)
    for rol in roles:
        for r in roles_fase:
            if rol.id==r.id:
                rol_usuario=rol
    if permiso=='' and rol_usuario!=None:
        return True
    if rol_usuario!=None:
        perm=Permission.objects.get(codename=permiso)
        permisos=Permission.objects.filter(group__id=rol_usuario.id)
        for p in permisos:
            if p==perm:
                return True

    return False


@login_required
def listar_tiposDeItem(request, id_fase):
    """
    vista para listar los tipos de item de las fases asignadas a un usuario de un proyecto especifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_fase: clave foranea a la fase
    @return render_to_response(...)
    """
    #se comprueba que el usuario sea miembro de esa fase, si no es alguien sin permisos
    flag=es_miembro(request.user.id, id_fase,'') # true si es mienbro de la fase

    fase=Fase.objects.get(id=id_fase)   #
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    if flag==True:
        tiposItem = TipoItem.objects.filter(fase_id=id_fase).order_by('nombre')
    else:
        return render_to_response('403.html')

    nivel = 2
    return render_to_response('items/listar_tipoDeItem.html', {'datos': tiposItem, 'fase':fase, 'nivel':nivel, 'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required
@permission_required('tipoItem')
def detalle_tiposDeItem(request, id_tipoItem):
    """
    Vista para ver los detalles del tipo de item <id_tipoItem>
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoItem: referencia al tipo de item dentro de la base de datos
    @return render_to_response('tiposDeItem/detalle_tipoDeItem.html', {'datos': dato, 'atributos': atributos},
                              context_instance=RequestContext(request))
    """
    dato = get_object_or_404(TipoItem, pk=id_tipoItem)
    fase = Fase.objects.get(id=dato.fase_id)
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)
    atributos = Atributo.objects.filter(tipoItem__id=id_tipoItem)
    return render_to_response('items/detalle_tipoDeItem.html', {'datos': dato, 'atributos': atributos,'fase':fase,'proyecto':proyecto},
                              context_instance=RequestContext(request))


def cantidad_items(id_tipoItem):
    """
    funcion para contar la cantidad de items ya creados en una fase
    Si aun no se alcanzo el limite devuelve True,
    Ademas verifica que la fase a agregar items no tenga estado FIN
    @param id_tipoItem: clave foranea al tipoItem
    @return: boolean
    """
    titem=get_object_or_404(TipoItem,id=id_tipoItem)
    fase=Fase.objects.get(id=titem.fase_id)
    if fase.estado=='FIN':
        return False
    item=Item.objects.filter(tipo_item_id=id_tipoItem)
    contador=0
    for i in item:
        contador+=1
    if contador<fase.maxItems:
        return True
    else:
        return False


def seleccion_tipoItem(request,id_fase):
    """
    funcion que determinara el tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_fase: clave foranea a la fase
    @return render_to_response('items/seleccion_TipoItem.html', { 'TipoItem':Titem, 'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
    """

    fase = Fase.objects.get(id=id_fase)
    #if fase.estado=='EJE':
    Titem=TipoItem.objects.filter(fase_id=fase.id)
    proyecto=Proyecto.objects.get(id=fase.proyecto_id)

    return render_to_response('items/seleccion_TipoItem.html', { 'TipoItem':Titem, 'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))


@login_required

def crear_item(request,id_tipoItem):
    """
    Vista para crear un item y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_tipoItem: clave foranea al tipoItem
    @ return render_to_response('items/...) o render_to_response('403.html')
    """
    atri=1
    if cantidad_items(id_tipoItem):
        print(cantidad_items(id_tipoItem))
        id_fase=TipoItem.objects.get(id=id_tipoItem).fase_id
        flag=es_miembro(request.user.id,id_fase,'add_item')
        atributos=Atributo.objects.filter(tipoItem=id_tipoItem)
        if len(atributos)==0:
            atri=0
        fase=Fase.objects.get(id=id_fase)
        proyecto=fase.proyecto_id
        items=[]
        tipoitem=[]
        fase_anterior=Fase.objects.filter(proyecto_id=proyecto, orden=((fase.orden)-1))
        if len(fase_anterior)==0:
            items=[]
        else:
            for fase in fase_anterior:
                titem=TipoItem.objects.filter(fase_id=fase.id)
                for i in titem:
                    it=Item.objects.filter(tipo_item_id=i.id, estado='FIN')
                    for ii in it:
                        items.append(ii)

        if flag==True:
            if request.method=='POST':
                #formset = ItemFormSet(request.POST)
                formulario = PrimeraFaseForm(request.POST)

                if formulario.is_valid():
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                    #obtener item con el cual relacionar
                    item_nombre=request.POST.get('entradalista')
                    if item_nombre!=None:
                        item=''
                        itemss=Item.objects.filter(nombre=item_nombre)
                        for i in itemss:
                            item=i
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=item.id, tipo='Sucesor',tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat,fase_id=id_fase)
                        newItem.save()
                    else:
                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1,tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat,fase_id=id_fase)
                        newItem.save()
                #guardar archivo
                    if request.FILES.get('file')!=None:
                        archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=cod.id)
                        archivo.save()
                #guardar atributos

                    for atributo in atributos:

                        a=request.POST.get(atributo.nombre)
                        if a!=None:
                            #validar atributos antes de guardarlos
                            #if validarAtributo(request,atributo.tipo,a):
                                aa=AtributoItem(id_item_id=cod.id, id_atributo=atributo,valor=a,version=1)
                                aa.save()
                    return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm()
                hijo=False
                proyecto=Proyecto.objects.filter(id=fase.proyecto_id)
                return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos, 'items':items, 'hijo':hijo,'atri':atri,'titem':id_tipoItem,'fase':fase}, context_instance=RequestContext(request))
        else:
            return render_to_response('403.html')
    else:
        id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
        return render_to_response('items/cantidad_maxima.html',{'id_fase':id_fase}, context_instance=RequestContext(request))


def puede_add_items(id_fase):
    """
    Funcion que verifica que ya se pueden agregar items a una fase. Si es la primera fase, se puede
    Si no, se verifica que la fase anterior tenga items en una linea base para poder agregar items a la
    fase siguiente.
    @param id_fase: clave foranea a la fase
    @return: boolean
    """
    fase=Fase.objects.get(id=id_fase)
    if fase.orden==1:
        return True
    else:
        fase_anterior=Fase.objects.get(orden=fase.orden-1,proyecto=fase.proyecto)
        tipoitem=TipoItem.objects.filter(fase_id=fase_anterior.id)

        for ti in tipoitem:
            item=Item.objects.filter(tipo_item_id=ti.id)
            for i in item:
                if i.estado=='FIN':
                    return True
    return False

@login_required

def listar_items(request,id_fase):
    """
    vista para listar los items pertenecientes a la fase
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea a la fase
    @return render_to_response(..) o HttpResponse(...)
    """
    titem=get_object_or_404(Fase,id=id_fase)
    fase=Fase.objects.filter(id=id_fase)
    if es_miembro(request.user.id,fase,''):
        items=Item.objects.filter(fase_id=id_fase)
        print(items)
        if puede_add_items(fase):
            nivel = 3
            id_proyecto=Fase.objects.get(id=fase).proyecto_id
            proyecto=Proyecto.objects.get(id=id_proyecto)
            return render_to_response('items/listar_items.html', {'datos': items, 'fase':titem, 'nivel':nivel,'proyecto':proyecto}, context_instance=RequestContext(request))
        else:
            #ESTE HAY QUE CORREGIR SI HAY TIEMPO
            return HttpResponse("<h1>No se pueden administrar los Items de esta fase. La fase anterior aun no tiene items finalizados<h1>")

    else:
        return render_to_response('403.html')

def generar_version(item):
    """
    funcion para generar y guardar una nueva version de un item a modificar
    @param item: item asociado
    """
    today = datetime.now() #fecha actual
    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    item_viejo=VersionItem(id_item=item, nombre=item.nombre, descripcion=item.descripcion, fecha_mod=dateFormat, version=item.version, costo=item.costo, tiempo=item.tiempo, tipo_item=item.tipo_item, relacion=item.relacion, tipo=item.tipo, estado=item.estado,lineaBase=item.lineaBase,fase=item.fase )
    item_viejo.save()


def editar_item(request,id_item):
    '''
    vista para cambiar el nombre y la descripcion del tipo de item, y ademas agregar atributos al mismo
    Si el item se encuentra con el estado CON (solicitud de cambio aprobada), se puede modificar el item solo si el
    usuario es el que realizo la solicittud de cambio
    '''
    id_tipoItem=get_object_or_404(Item,id=id_item).tipo_item_id
    id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
    flag=es_miembro(request.user.id,id_fase,'cambiar_item')
    item_nuevo=get_object_or_404(Item,id=id_item)
    atri=1
    if flag==False:
        return HttpResponseRedirect('/denegado')

    atributos=AtributoItem.objects.filter(id_item=id_item)
    if len(atributos)==0:
        atri=0
    if item_nuevo.estado=='CON':
        archivos=Archivo.objects.filter(id_item=item_nuevo)
        solicitudes=Solicitud.objects.filter(item=item_nuevo, estado='APROBADA')
        solicitud=solicitudes[0]
        solicitante=solicitud.usuario
        if request.user==solicitante:
            if request.method=='POST':
                formulario = PrimeraFaseForm(request.POST, instance=item_nuevo)

                if formulario.is_valid():

                    if request.FILES.get('file')!=None:
                        archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=id_item)
                        archivo.save()
                    #generar_version(item_nuevo,request.user)
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                    formulario.save()
                    item_nuevo.fecha_mod=dateFormat
                    #item_nuevo.version=item_nuevo.version+1
                    item_nuevo.save()

                    for atributo in atributos:

                        a=request.POST[atributo.id_atributo.nombre]
                        if a!=None:
                            #validar atributos antes de guardarlos
                            validar=True
                            if atributo.id_atributo.tipo == "FEC":
                                try:
                                    fecha = datetime.strptime(str(a), '%d/%m/%Y')
                                except ValueError:
                                    validar=False
                            else:
                                if atributo.id_atributo.tipo == "NUM":
                                    a = a.isdigit()
                                    if not a:
                                        validar=False

                                else:
                                    if atributo.id_atributo.tipo == "LOG":
                                        if a != "Verdadero" and a != "Falso":
                                            validar=False

                            if validar==True:
                                aa=AtributoItem.objects.get(id=atributo.id)
                                aa.valor=a
                                aa.save()
                    return render_to_response('items/creacion_correcta.html',{'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))
            else:

                formulario = PrimeraFaseForm(instance=item_nuevo)
            return render_to_response('items/modificar_item_solicitud.html', { 'formulario': formulario, 'item':item_nuevo,'titem':id_tipoItem, 'atributos':atributos, 'atri':atri, 'archivos':archivos}, context_instance=RequestContext(request))
        else:
            return HttpResponseRedirect ('/denegado')

    if flag==True and item_nuevo.estado=='BLO':
        return HttpResponse('<h1> No se puede modificar el item, ya que ya ha sido generada una solicitud de cambio para el mismo</h1>')

    if flag==True and item_nuevo.estado=='FIN':
        return render_to_response('solicitudes/modificar_finalizado.html',{'id_item':item_nuevo.id, 'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))
    if item_nuevo.estado=='PEN':

        if flag==True:

                if request.method=='POST':

                    formulario = PrimeraFaseForm(request.POST, instance=item_nuevo)

                    if formulario.is_valid():
                        generar_version(item_nuevo,request.user)
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format

                        formulario.save()
                        item_nuevo.fecha_mod=dateFormat
                        item_nuevo.version=item_nuevo.version+1
                        item_nuevo.save()

                        return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase, 'id_tipo_item':id_tipoItem}, context_instance=RequestContext(request))

                else:

                    formulario = PrimeraFaseForm(instance=item_nuevo)
                    hijo=True
                return render_to_response('items/editar_item.html', { 'formulario': formulario, 'item':item_nuevo,'titem':id_tipoItem}, context_instance=RequestContext(request))

        else:
                return render_to_response('403.html')
    else:
        return HttpResponse('<h1> No se puede modificar el item, ya que su estado no es Pendiente</h1>')

@login_required
###################FALTA CORREGIR VOLVER A CARGAR
def listar_archivos(request, id_item):
    """
    vista para gestionar los archivos de un item dado
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response(..)
    """

    titem=get_object_or_404(Item,id=id_item).tipo_item
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'change_item'):
        archivos=Archivo.objects.filter(id_item=id_item)
        if request.method=='POST':
            if request.FILES.get('file')!=None:
                archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=id_item)
                archivo.save()

        fase=Fase.objects.get(id=titem.fase_id)
        proyecto=Proyecto.objects.get(id=fase.proyecto_id)
        return render_to_response('items/listar_archivos.html', { 'archivos': archivos,'titem':id_item,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')

@login_required

def eliminar_archivo(request, id_archivo):
    """
    vista que recibe el id de un archivo y lo borra de la base de datos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_archivo: clave foranea al archivo a eliminar
    @return HttpResponseRedirect('/desarrollo/item/archivos/'+str(item.id))
    """

    archivo=get_object_or_404(Archivo,id=id_archivo)
    item=archivo.id_item
    archivo.delete()
    return HttpResponseRedirect('/desarrollo/item/archivos/'+str(item.id))

@login_required
def detalle_item(request, id_item):
    """
    vista para ver los detalles del item <id_item>
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response(..)
    """
    item=get_object_or_404(Item,id=id_item)
    tipoitem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=tipoitem.fase_id
    fasse=Fase.objects.get(id=fase)
    proyecto=Proyecto.objects.get(id=fasse.proyecto_id)
    if es_miembro(request.user.id, fase,''):
        atributos=AtributoItem.objects.filter(id_item=id_item)
        archivos=Archivo.objects.filter(id_item=id_item)
        dato = get_object_or_404(Item, pk=id_item)

        return render_to_response('items/detalle_item.html', {'datos': dato, 'atributos': atributos, 'archivos':archivos,'fase':fasse,'proyecto':proyecto}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')

@login_required
def listar_versiones(request,id_item):
    '''
    vista para listar todas las versiones existentes de un item dado
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return HttpResponseRedirect('/desarrollo/item/archivos/'+str(item.id))
    '''
    item=get_object_or_404(Item,id=id_item)
    titem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'change_versionitem'):
        items=VersionItem.objects.filter(id_item_id=id_item).order_by('version')
        return render_to_response('items/listar_versiones.html', {'datos': items, 'titem':titem,'item':item}, context_instance=RequestContext(request))


    else:
        return render_to_response('403.html')

@login_required
def detalle_version_item(request, id_version):
    """
    vista para ver los detalles del item <id_item>
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response(..)
    """
    item=get_object_or_404(VersionItem,id=id_version)
    tipoitem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=tipoitem.fase_id
    if es_miembro(request.user.id, fase,''):
        dato = get_object_or_404(VersionItem, pk=id_version)

        return render_to_response('items/detalle_version.html', {'datos': dato,'item':item}, context_instance=RequestContext(request))
    else:
        return render_to_response('403.html')

def volver_item(version,rel):
    """
    funcion que vuelve a  una version anterior de un item dado
    @param version: version a comprobar
    @param rel: relacion
    """
    today = datetime.now() #fecha actual
    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
    item=get_object_or_404(Item,id=version.id_item_id)
    item.version=item.version+1
    item.nombre=version.nombre
    item.descripcion=version.descripcion
    item.costo=version.costo
    item.tiempo=version.tiempo
    item.tipo=version.tipo
    if rel==0:
        item.relacion=version.relacion
    else:
        item.relacion=rel
    item.fecha_mod=dateFormat
    item.save()

def comprobar_relacion(version):
    """
    comprueba que el item a reversionar este relacionado con un item que aun esta activo (true)
    de lo contrario (false)
    Ademas comprueba que no se formen ciclos al modificar una relacion del tipo padre-hijo
    @param version: version a comprobar
    """

    if version.relacion==None:
        return True
    relacion=get_object_or_404(Item,id=version.relacion_id)

    item=version.id_item
    a=Item.objects.filter((Q(tipo='Hijo') & Q(relacion=item) & Q(id=relacion.id)) & (Q (estado='PEN') | Q(estado='FIN')  | Q(estado='VAL')))
    if a!=None:
        return False
    items=Item.objects.filter(estado='ANU')
    for i in items:
        if i==relacion:
            return False
    return True

@login_required

def reversionar_item(request, id_version):
    """
    vista para volver a una version anterior de un item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response('items/creacion_correcta.html', ...) o render_to_response('403.html')
    """
    version=get_object_or_404(VersionItem,id=id_version)
    item=get_object_or_404(Item,id=version.id_item_id)

    titem=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=titem.fase_id
    if es_miembro(request.user.id,fase,'change_versionitem'):
        version=get_object_or_404(VersionItem,id=id_version)
        item=get_object_or_404(Item,id=version.id_item_id)
        generar_version(item)
        #comprueba la relacion
        if comprobar_relacion(version):

            volver_item(version,0)
            fase=Fase.objects.get(id=fase)
            return render_to_response('items/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))
        else:
                volver_item(version,item.relacion)
                fase=Fase.objects.get(id=fase) ##################VER reacion_correcta_relacion
                return render_to_response('items/creacion_correcta.html',{'id_fase':fase.id}, context_instance=RequestContext(request))


    else:
        return render_to_response('403.html')


def descargar(idarchivo):
    """
    Funcion que recibe el id de un archivo y retorna el objeto archivo dado el id recibido
    @param idarchivo: clave al archivo
    @return archivo.archivo
    """
    archivo=get_object_or_404(Archivo,id=idarchivo)

    return archivo.archivo

@login_required
def descargo_archivo(request, idarchivo):
    """
    Vista para descargar un archivo de un item especifico
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al archivo a cargar
    @return StreamingHttpResponse(descargar(idarchivo),content_type='application/force-download')
    """
    return StreamingHttpResponse(descargar(idarchivo),content_type='application/force-download')

@login_required

def crear_item_hijo(request,id_item):
    """
    Vista para crear un item como hijo de uno ya creado y asignarlo a un tipo de item. Ademas se dan las opciones de agregar un
    archivo al item, y de completar todos los atributos de su tipo de item
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response('items/...) o HttpResponse(...)
    """
    item=get_object_or_404(Item,id=id_item)
    if item.estado=='FIN' or item.estado=='VAL' or item.estado=='PEN':
        atri=1
        id_tipoItem=get_object_or_404(Item,id=id_item).tipo_item_id
        if cantidad_items(id_tipoItem):
            id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
            flag=es_miembro(request.user.id,id_fase,'agregar_item')
            atributos=Atributo.objects.filter(tipoItem=id_tipoItem)
            if len(atributos)==0:
                atri=0
            fase=get_object_or_404(Fase,id=id_fase)
            proyecto=fase.proyecto_id
            if flag==True:
                if request.method=='POST':
                    #formset = ItemFormSet(request.POST)
                    formulario = PrimeraFaseForm(request.POST)

                    if formulario.is_valid():
                        today = datetime.now() #fecha actual
                        dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                        #obtener item con el cual relacionar

                        cod=newItem=Item(nombre=request.POST['nombre'],descripcion=request.POST['descripcion'],costo=request.POST['costo'],tiempo=request.POST['tiempo'],estado='PEN',version=1, relacion_id=id_item, tipo='Hijo',tipo_item_id=id_tipoItem,fecha_creacion=dateFormat, fecha_mod=dateFormat,fase_id=id_fase)

                        newItem.save()
                    #guardar archivo
                        if request.FILES.get('file')!=None:
                            archivo=Archivo(archivo=request.FILES['file'],nombre='', id_item_id=cod.id)
                            archivo.save()
                    #guardar atributos
                        for atributo in atributos:

                            a=request.POST[atributo.nombre]
                            #validar atributos antes de guardarlos
                            #if validarAtributo(request,atributo.tipo,a):
                            aa=AtributoItem(id_item_id=cod.id, id_atributo=atributo,valor=a,version=1)
                            aa.save()
                        return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
                else:

                    formulario = PrimeraFaseForm()
                    hijo=True
                    return render_to_response('items/crear_item.html', { 'formulario': formulario, 'atributos':atributos,'hijo':hijo,'atri':atri,'titem':id_tipoItem,'fase':fase}, context_instance=RequestContext(request))
            else:
                return render_to_response('403.html')
        else:
            id_fase=get_object_or_404(TipoItem,id=id_tipoItem).fase_id
            return render_to_response('items/cantidad_maxima.html',{'id_fase':id_fase}, context_instance=RequestContext(request))
    else:
        return HttpResponse("<h1>No se puede crear un hijo a un item con estado que no sea Finalizado, Pendiente o Validado</h1>")


@login_required
def cambiar_estado_item(request,id_item):
    """
    vista para cambiar el estado de un item, teniendo en cuenta:
    1) Si se quiere pasar de PEN  a VAL, se verifica que el estado de su padre tambien sea VAL
    2) Si se quiere pasar de VAL a PEN se verifica que el estado de sus hijos tambien sea PEN
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response('items/...) de acuerdo a los diferentes estados que puede tener un item
    """

    item=get_object_or_404(Item,id=id_item)
    id_fase=get_object_or_404(Item,id=id_item).fase_id
    fase=Fase.objects.get(id=id_fase)
    proyecto=Proyecto.objects.get(id=id_fase)
    nombre=item.nombre
    titem=item.tipo_item_id
    if request.method == 'POST':
        bandera=False
        item_form = EstadoItemForm(request.POST, instance=item)
        if item_form.is_valid():
                    if item_form.cleaned_data['estado']=='VAL':
                        if item.tipo=='Hijo':
                            papa=item.relacion
                            if papa.estado=='PEN':
                                #'No se puede cambiar a Validado ya que su padre no ha sido validado o Finalizado'
                                return render_to_response('items/cambiar_estado_item.html', { 'item_form': item_form, 'nombre':nombre, 'titem':item,'mensaje':0,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
                                bandera=True
                            if papa.estado=='VAL':
                                bandera=False
                    if item_form.cleaned_data['estado']=='PEN':
                            hijos=Item.objects.filter(relacion=item)
                            for hijo in hijos:
                                if hijo.estado!='PEN' and hijo.tipo=='Hijo':
                                    # 'No se puede cambiar  a pendiente ya que tiene hijos con estados distintos a Pendiente'
                                    return render_to_response('items/cambiar_estado_item.html', { 'item_form': item_form, 'nombre':nombre, 'titem':item,'mensaje':1,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
                                    bandera=True
                    if bandera==True:
                        return render_to_response('items/cambiar_estado_item.html', { 'item_form': item_form, 'nombre':nombre, 'titem':item,'mensaje':100,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))
                    else:
                        item_form.save()
                        return render_to_response('items/creacion_correcta.html',{'id_fase':id_fase}, context_instance=RequestContext(request))

    else:
        # formulario inicial
        item_form = EstadoItemForm(instance=item)
        return render_to_response('items/cambiar_estado_item.html', { 'item_form': item_form, 'nombre':nombre,'titem':item,'mensaje':100,'fase':fase,'proyecto':proyecto}, context_instance=RequestContext(request))

@login_required

def cambiar_padre(request, id_item):
    """
    Cambia la relacion padre-hijo de los items
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response('items/cambiar_padres.html', { 'items':items, 'tipoitem':item, 'fase':fase}, context_instance=RequestContext(request)) o return HttpResponseRedirect('/denegado')
    """
    item=get_object_or_404(Item,id=id_item)
    tipo=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fase=get_object_or_404(Fase,id=tipo.fase_id)
    proyecto=Proyecto.objects.get(id=fase.id)
    if es_miembro(request.user.id,fase.id,'cambiar_item'):
        items=[]
        titem=TipoItem.objects.filter(fase_id=fase.id)
        for i in titem:
            a=Item.objects.filter(Q(tipo_item_id=i.id) & (Q (estado='PEN') | Q(estado='FIN')  | Q(estado='VAL')))
            for aa in a:
                #verifica que el item a relacionar no sea si mismo, su hijo o ya sea su padre
                if aa != item and item.relacion!=aa and item!=aa.relacion:
                    items.append(aa)
        if request.method=='POST':
            item_nombre=request.POST.get('entradalista')
            if item_nombre!=None:

                    item_rel=''
                    today = datetime.now() #fecha actual
                    dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                    item=get_object_or_404(Item,id=id_item)
                    generar_version(item)
                    item.fecha_mod=dateFormat
                    item.version=item.version+1
                    itemss=Item.objects.filter(nombre=item_nombre)
                    for i in itemss:
                        item_rel=i
                    item.relacion=item_rel
                    item.tipo='Hijo'
                    item.save()
                    return HttpResponseRedirect('/desarrollo/item/listar/'+str(item.fase_id))
        if len(items)==0:
            messages.add_message(request,settings.DELETE_MESSAGE, "No hay otros items que pueden ser padres de este")
        return render_to_response('items/cambiar_padres.html', { 'items':items, 'tipoitem':item, 'fase':fase}, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/denegado')

@login_required

def cambiar_antecesor(request, id_item):
    """
    vista para cambiar la relacion de un item, del tipo antecesor
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_item: clave foranea al item
    @return render_to_response('items/cambiar_antecesor.html', { 'items':items, 'tipoitem':item,'fase':fas,'proyecto':proyecto}, context_instance=RequestContext(request))
    """
    item=get_object_or_404(Item,id=id_item)
    tipo=get_object_or_404(TipoItem,id=item.tipo_item_id)
    fas=get_object_or_404(Fase,id=tipo.fase_id)
    proyecto=Proyecto.objects.get(id=fas.proyecto_id)
    #if es_miembro(request.user.id,fas.id,'editar_item'):
    proyecto=fas.proyecto_id
    items=[]
    fase_anterior=Fase.objects.filter(proyecto_id=proyecto, orden=fas.orden-1)
    if len(fase_anterior)==0:
        items=[]
    else:
        for fase in fase_anterior:
            titem=TipoItem.objects.filter(fase_id=fase.id)
            for i in titem:
                ii=Item.objects.filter(tipo_item_id=i.id, estado='FIN')
                for it in ii:
                    if it!=item.relacion:
                        items.append(it)
    if request.method=='POST':
        item_nombre=request.POST.get('entradalista')
        if item_nombre!=None:
                today = datetime.now() #fecha actual
                dateFormat = today.strftime("%Y-%m-%d") # fecha con format
                generar_version(item)
                item.fecha_mod=dateFormat
                item.version=item.version+1
                item_rel=Item.objects.get(nombre=item_nombre)
                item.relacion=item_rel
                item.tipo='Sucesor'
                item.save()
                return HttpResponseRedirect('/desarrollo/item/listar/'+str(item.tipo_item_id))
    if len(items)==0:
        messages.add_message(request,settings.DELETE_MESSAGE, "No hay otros items que pueden ser antecesores de este")
    return render_to_response('items/cambiar_antecesor.html', { 'items':items, 'tipoitem':item,'fase':fas,'proyecto':proyecto}, context_instance=RequestContext(request))
#else:
#  print('entro')
# return HttpResponseRedirect('/denegado')

def dibujarProyecto(proyecto):
    '''
    Funcion que grafica los items con sus relaciones de un proyecto dado
    '''
    #inicializar estructuras
    grafo = pydot.Dot(graph_type='digraph',fontname="Verdana",rankdir="LR")
    fases = Fase.objects.filter(proyecto_id=proyecto).order_by('orden')
    clusters = []
    clusters.append(None)
    for fase in fases:
        if(fase.estado=='FIN'):
            cluster = pydot.Cluster(str(fase.orden),
                                    label=str(fase.orden)+") "+fase.nombre,
                                    style="filled",
                                    fillcolor="gray")
        else:
            cluster = pydot.Cluster(str(fase.orden),
                                    label=str(fase.orden)+") "+fase.nombre)
        clusters.append(cluster)

    for cluster in clusters:
        if(cluster!=None):
            grafo.add_subgraph(cluster)


    lista=itemsProyecto(proyecto)
    items=[]
    for item in lista:
        if item.estado!="ANU":
            items.append(item)
    #agregar nodos
    for item in items:

        if item.estado=="PEN":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="gray",
                                                                 fontcolor="black"))
        elif item.estado=="VAL":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="blue",
                                                                 fontcolor="white"))
        elif item.estado=="FIN":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="green",
                                                                 fontcolor="white"))
        elif item.estado=="REV":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="red",
                                                                 fontcolor="white"))
        elif item.estado=="CON":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="yellow",
                                                                 fontcolor="white"))
        elif item.estado=="BLO":
            clusters[item.tipo_item.fase.orden].add_node(pydot.Node(str(item.id),
                                                                 label=item.nombre,
                                                                 style="filled",
                                                                 fillcolor="magenta",
                                                                 fontcolor="white"))
    #agregar arcos
    for item in items:
        relaciones = Item.objects.filter(relacion=item).exclude(estado='ANU')
        if relaciones!=None:
            for relacion in relaciones:
                grafo.add_edge(pydot.Edge(str(item.id),str(relacion.id),label='costo='+str(item.costo) ))

    date=datetime.now()

    name=str(date)+'grafico.jpg'
    grafo.write_jpg(str(settings.BASE_DIR)+'/static/img/'+str(name))
    return name

def recorridoEnProfundidad(item):
    '''
    Funcion que llama a recorrer items en profundidad
    y retorna un vector con la suma del costo y del tiempo
    '''
    titem=item.tipo_item
    fase=titem.fase
    proyecto=fase.proyecto
    listaitems =itemsProyecto(proyecto)
    maxiditem = getMaxIdItemEnLista(listaitems)
    global sumaCosto, sumaTiempo,visitados
    visitados = [0]*(maxiditem+1)
    sumaCosto=0
    sumaTiempo=0
    recorrer(item.id)
    ret = [sumaCosto,sumaTiempo]
    return ret

def recorrer(id_item):
    '''
    Funcion para recorrer el grafo de items del proyecto en profundidad
    Sumando el costo y el tiempo de cada uno
    '''
    global sumaCosto, sumaTiempo, visitados
    visitados[id_item]=1
    item=get_object_or_404(Item,id=id_item)
    sumaCosto = sumaCosto + item.costo
    sumaTiempo = sumaTiempo + item.tiempo
    relaciones = Item.objects.filter(relacion=item.id)
    for relacion in relaciones:
        if(visitados[relacion.id]==0):
            recorrer(relacion.id)

def getMaxIdItemEnLista(lista):
    '''
    Funcion para hallar el id maximo de los items de una lista
    '''
    max=0
    for item in lista:
        if item.id>max:
            max=item.id
    return max



def crear_solicitud(request,id_item):
    '''
    Vista para la creacion de una solicitud de cambio para un item especificado en id_item
    '''
    item=get_object_or_404(Item,id=id_item)
    id_tipoItem=item.tipo_item.id
    fase=item.tipo_item.fase
    proyecto=fase.proyecto
    costotiempo=recorridoEnProfundidad(item)
    costo=costotiempo[0]
    tiempo=costotiempo[1]
    if es_miembro(request.user.id,fase.id,'agregar_solicitudcambio')!=True or item.estado!='FIN':
        return HttpResponseRedirect('/denegado')
    if request.method=='POST':
        formulario = SolicitudCambioForm(request.POST)
        if formulario.is_valid():
            today = datetime.now()
            dateFormat = today.strftime("%Y-%m-%d")
            usuario=request.user
            solicitud=Solicitud(nombre=request.POST['nombre'], descripcion=request.POST['descripcion'],item=item,proyecto=proyecto,usuario=usuario,fecha=dateFormat, costo=costo, tiempo=tiempo,estado='PENDIENTE')
            solicitud.save()
            item.estado='BLO'
            item.save()
            return HttpResponseRedirect('/desarrollo/item/listar/'+str(item.fase_id))
    else:
        formulario=SolicitudCambioForm()
    return render_to_response('solicitudes/crear_solicitud.html',{'titem':id_tipoItem,'costo':costo, 'tiempo':tiempo, 'item':item, 'proyecto':proyecto, 'fase':fase,'formulario':formulario}, context_instance=RequestContext(request))