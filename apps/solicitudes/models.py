__author__ = 'teaser'

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from apps.items.models import Item

ESTADOS = (
    ('RECHAZADA','Rechazada'),
    ('APROBADA','Aprobada'),
    ('PENDIENTE','Pendiente'),
    ('EJECUTADA', 'Ejecutada')
)

VOTO = (
    ('APROBAR','A Favor'),
    ('RECHAZAR','En contra'),

)


class Solicitud(models.Model):

    """
    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar nombre: Cadena de caracteres
    @cvar descripcion: Un campo de texto
    @cvar  fecha_solicitud: Fecha en que se expidio la solicitud
    @cvar estado: Enum de los tipos de estados por los que puede pasar una solicitud: Pendiente, Anulado, Activo y Finalizado
    @cvar fase: Clave foranea a la tabla Fase
    @cvar voto: Clave foranea a la tabla Voto
    """

    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    proyecto=models.ForeignKey(Proyecto)
    item=models.ForeignKey(Item)
    fecha=models.DateField(verbose_name='Fecha de Solicitud')
    costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    usuario=models.ForeignKey(User)
    estado=models.CharField(max_length=10, verbose_name='Estado',choices=ESTADOS)



class Voto(models.Model):

    """
    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar solicitud: Clave foranea a la tabla Solicitud
    @cvar usuario: Clave foranea a la tabla User
    @cvar estado: Enum de los tipos de estados por los que puede pasar un proyecto: Pendiente, Aprobada, Rechazada y Ejecutada
    @cvar observaciones: Un campo de texto
    @cvar comite: Relacion muchos a muchos con la tabla User
    """

    solicitud=models.ForeignKey(Solicitud)
    usuario=models.ForeignKey(User)
    voto=models.CharField(max_length=10, verbose_name='Voto',choices=VOTO, null=False)

class ItemsARevision(models.Model):
    item_bloqueado=models.ForeignKey(Item, unique=False, related_name='item_bloqueado')
    item_revision=models.ForeignKey(Item, related_name='item_revision')

