# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required, permission_required
from django.utils import timezone
from datetime import datetime
from apps.proyectos.forms import ProyectoForm, CambiarEstadoForm
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from apps.proyectos.models import Proyecto
from apps.fases.models import Fase
from apps.inicio.models import Perfiles
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib import messages
from SIAP import settings
from apps.tiposDeItem.models import TipoItem

__author__ = 'alvarenga'
__text__ = 'Este modulo contiene funciones que permiten el control de proyectos'


@login_required
@permission_required('proyectos')
def registrar_proyecto(request):
    """
    Vista para registrar un nuevo proyecto con su lider y miembros de su comite de cambios
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return HttpResponseRedirect('/proyectos/register/success') si el rol líder fue correctamente asignado o
    render_to_response('proyectos/registrar_proyecto.html',{'formulario':formulario}, context_instance=RequestContext(request)) al formulario
    """

    if request.method == 'POST':
        formulario = ProyectoForm(request.POST)

        if formulario.is_valid():
            fecha = datetime.strptime(str(request.POST["fecha_ini"]), '%d/%m/%Y')#convert string to datetime
            fecha = fecha.strftime('%Y-%m-%d')# fecha con formato
            fecha1 = datetime.strptime(fecha, '%Y-%m-%d')#convert string to datetime

            fechaf = datetime.strptime(str(request.POST["fecha_fin"]), '%d/%m/%Y')#convert string to datetime
            fechaf = fechaf.strftime('%Y-%m-%d')# fecha con formato
            fecha2 = datetime.strptime(fechaf, '%Y-%m-%d') #convert string to datetime

            fecha_actual = datetime.now() #fecha actual
            fecha_actual = fecha_actual.strftime('%Y-%m-%d')#fecha con formato
            if datetime.strptime(fecha_actual, '%Y-%m-%d') > fecha1:
                return render_to_response('proyectos/registrar_proyecto.html', {'formulario': formulario, 'mensaje': 1},
                                          context_instance=RequestContext(request))
            elif fecha1 > fecha2:
                return render_to_response('proyectos/registrar_proyecto.html', {'formulario': formulario, 'mensaje': 0},
                                          context_instance=RequestContext(request))
            else:
                lider = formulario.cleaned_data['lider']
                Eslider=Perfiles.objects.get(usuario=lider)
                #Verifica si esta puede ser lider
                if Eslider.lider != True:
                    return render_to_response('proyectos/registrar_proyecto.html', {'formulario': formulario, 'mensaje': 2},
                                          context_instance=RequestContext(request))
                #asigna el rol lider al usuario seleccionado
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
                formulario.save()
                return HttpResponseRedirect('/proyectos/register/success')
    else:
        formulario = ProyectoForm()
    return render_to_response('proyectos/registrar_proyecto.html', {'formulario': formulario, 'mensaje': 1000},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def importar_proyecto(request, id_proyecto):
    """
    Vista para importar un proyectos, dado en <id_proyecto>  con su lider y miembros del comite
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return HttpResponseRedirect('/proyectos/register/success') si
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    if request.method == 'POST':
        formulario = ProyectoForm(request.POST,
                                  initial={'nombre': proyecto.nombre, 'observaciones': proyecto.observaciones,
                                           'descripcion': proyecto.descripcion, 'fecha_ini': proyecto.fecha_ini,
                                           'fecha_fin': proyecto.fecha_fin})

        #verifica que la fecha de inicio sea menor a la de fin
        if formulario.is_valid():
            if formulario.cleaned_data['fecha_ini'] > formulario.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE,
                                     "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider = formulario.cleaned_data['lider']
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
                formulario.save()
                return HttpResponseRedirect('/proyectos/register/success')
    else:
        formulario = ProyectoForm(initial={'nombre': proyecto.nombre, 'observaciones': proyecto.observaciones,
                                           'descripcion': proyecto.descripcion, 'fecha_ini': proyecto.fecha_ini,
                                           'fecha_fin': proyecto.fecha_fin})
    return render_to_response('proyectos/registrar_proyecto.html', {'formulario': formulario},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def RegisterSuccessView(request):
    """
    Vista llamada en caso de creación correcta de un proyecto, redirige a un template de éxito
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/creacion_correcta.html', context_instance=RequestContext(request))
    """
    return render_to_response('proyectos/creacion_correcta.html', context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def RegisterFailedView(request, id_proyecto):
    """
    Vista que retorna a un template de fracaso en caso de que el proyectos no pueda cambiar de estado
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto}, context_instance=RequestContext(request))
    """
    return render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def detalle_proyecto(request, id_proyecto):
    """
    Vista para ver los detalles del proyecto del sistema, junto con su líder y los miembros del comité
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato, 'comite': comite, 'lider':lider}, context_instance=RequestContext(request))
    """

    dato = get_object_or_404(Proyecto, pk=id_proyecto)
    comite = User.objects.filter(comite__id=id_proyecto)
    lider = get_object_or_404(User, pk=dato.lider_id)
    return render_to_response('proyectos/detalle_proyecto.html', {'proyecto': dato, 'comite': comite, 'lider': lider},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def listar_proyectos(request):
    """
    vista para listar los proyectos del sistema junto con el nombre de su lider
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos}, context_instance=RequestContext(request))
    """

    proyectos = Proyecto.objects.all().exclude(estado='ELI')

    return render_to_response('proyectos/listar_proyectos.html', {'datos': proyectos},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def buscar_proyecto(request):
    """
    vista para buscar los proyectos del sistema
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @return: render_to_response('proyectos/listar_proyectos.html', {'datos': results}, context_instance=RequestContext(request))
    """
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(nombre__contains=query)
        )
        results = Proyecto.objects.filter(qset).distinct()

    else:
        results = []

    return render_to_response('proyectos/listar_proyectos.html', {'datos': results},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def editar_proyecto(request, id_proyecto):
    """
    Vista para editar un proyecto,o su líder o los miembros de su comité
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: HttpResponseRedirect('/proyectos/register/success/') cuando el formulario es validado correctamente o render_to_response('proyectos/editar_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """
    proyecto = Proyecto.objects.get(id=id_proyecto)
    nombre = proyecto.nombre
    if request.method == 'POST':
        # formulario enviado
        proyecto_form = ProyectoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
            if proyecto_form.cleaned_data['fecha_ini'] > proyecto_form.cleaned_data['fecha_fin']:
                messages.add_message(request, settings.DELETE_MESSAGE,
                                     "Fecha de inicio debe ser menor a la fecha de finalizacion")
            else:
                lider = proyecto_form.cleaned_data['lider']
                roles = Group.objects.get(name='Lider')
                lider.groups.add(roles)
                # formulario validado correctamente
                proyecto_form.save()
                return HttpResponseRedirect('/proyectos/register/success/')
    else:
        # formulario inicial
        proyecto_form = ProyectoForm(instance=proyecto)
    return render_to_response('proyectos/editar_proyecto.html', {'proyectos': proyecto_form, 'nombre': nombre},
                              context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def cambiar_estado_proyecto(request, id_proyecto):
    """
    Vista para cambiar el estado de un proyecto, verificando que esto sea posible: para estar activo debe tener la cantidad
    necesaria de miembros del comité (cantidad impar)
    Si cambia a activo todas sus fases pasan al estado activo
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/cambiar_estado_proyecto.html', { 'proyectos': proyecto_form, 'nombre':nombre}, context_instance=RequestContext(request))
    """

    proyecto = Proyecto.objects.get(id=id_proyecto)
    nombre = proyecto.nombre
    comite = User.objects.filter(comite__id=id_proyecto)

    if request.method == 'POST':
        proyecto_form = CambiarEstadoForm(request.POST, instance=proyecto)
        if proyecto_form.is_valid():
            if proyecto_form.cleaned_data['estado'] == 'ACT':
                cantidad = 0
                for miembros in comite:
                    cantidad += 1
                if cantidad % 2 == 0:
                    return render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto},
                                              context_instance=RequestContext(request))
                if cantidad < 3:
                    return render_to_response('proyectos/cambio_estado_fallido.html', {'dato': id_proyecto},
                                              context_instance=RequestContext(request))
                fases = Fase.objects.filter(proyecto_id=id_proyecto)
                #obtener todos los roles del proyectos
                roles = []
                contador = 0
                flag = 0
                for fase in fases:
                    rol = Group.objects.filter(fase__id=fase.id)
                    for a in rol:
                        roles.append(a)
                for usuarios in comite:
                    flag = 0
                    g = Group.objects.filter(user__id=usuarios.id)

                    for gg in g:

                        for rr in roles:

                            if gg.id == rr.id:
                                flag = 1
                                break
                        if flag == 1:
                            contador += 1
                            flag = 0
                            break

                if contador != comite.count():
                    return render_to_response('proyectos/cambio_estado_fallido_nocomite.html', {'dato': id_proyecto},
                                              context_instance=RequestContext(request))

                if (fases.count() == 0):
                    return render_to_response('proyectos/cambio_estado_fallido_nofases.html', {'dato': id_proyecto},
                                              context_instance=RequestContext(request))
                for fase in fases:
                    tipoItem = TipoItem.objects.filter(fase_id=fase.id)
                    if tipoItem.count() == 0:
                        return render_to_response('proyectos/cambio_estado_fallido_notipositem.html',
                                                  {'dato': id_proyecto, 'fase': fase},
                                                  context_instance=RequestContext(request))

                for fase in fases:
                    fase.estado = 'EJE'
                    fase.save()
                # formulario validado correctamente
                proyecto_form.save()
                return HttpResponseRedirect('/proyectos/register/success/')
            else:
                if proyecto_form.cleaned_data['estado'] == 'ANU' or proyecto_form.cleaned_data['estado'] == 'PEN' or \
                                proyecto_form.cleaned_data['estado'] == 'ELI':
                    proyecto_form.save()
                    return HttpResponseRedirect('/proyectos/register/success/')

    else:
        # formulario inicial
        proyecto_form = CambiarEstadoForm(instance=proyecto)
        return render_to_response('proyectos/cambiar_estado_proyecto.html',
                                  {'proyectos': proyecto_form, 'nombre': nombre},
                                  context_instance=RequestContext(request))


@login_required
@permission_required('proyectos')
def ver_equipo(request, id_proyecto):
    """
    vista para ver todos los usuarios que forman parte de un proyectos
    @param request: objeto HttpRequest que representa la metadata de la solicitud HTTP
    @param id_proyecto: referencia al proyecto de la base de datos
    @return: render_to_response('proyectos/ver_equipo.html', {'proyectos':dato,'lider': lider, 'comite':comite, 'usuarios':usuarios}, context_instance=RequestContext(request))
    """
    dato = get_object_or_404(Proyecto, pk=id_proyecto)
    comite = User.objects.filter(comite__id=id_proyecto)
    lider = get_object_or_404(User, pk=dato.lider_id)
    fases = Fase.objects.filter(proyecto_id=id_proyecto)
    nombre_roles = []
    usuarios = []
    for fase in fases:
        roles = Group.objects.filter(fase__id=fase.id)
        for rol in roles:
            nombre_roles.append(rol)
            #for nombre in nombre_roles:
            u = User.objects.filter(groups__id=rol.id)

            for user in u:
                uu = user.first_name + " " + user.last_name + "  -  " + rol.name + " en la fase   " + fase.nombre + "\n"
                usuarios.append(uu)
    return render_to_response('proyectos/ver_equipo.html',
                              {'proyectos': dato, 'lider': lider, 'comite': comite, 'usuarios': usuarios},
                              context_instance=RequestContext(request))
