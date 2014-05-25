__author__ = 'teaser'

from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from apps.fases.models import Fase

ESTADOS = (

    ('PEN', 'Pendiente'),
    ('APR','Aprobada'),
    ('REC', 'Rechazada'),
    ('REA','Ejecutada')
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

    nombre= models.CharField(max_length=100, verbose_name='Nombre',unique=True)
    descripcion= models.TextField(verbose_name='Descripcion')
    fecha_solicitud=models.DateField(verbose_name='Fecha de solicitud',null=False)
    estado=models.CharField(max_length=3,choices= ESTADOS, default='PEN')
    #fase= models.ForeignKey(Fase, related_name='fase')
    #voto = models.ForeignKey(Voto, verbose_name = "votacion" )



class Voto(models.Model):

    """
    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar solicitud: Clave foranea a la tabla Solicitud
    @cvar usuario: Clave foranea a la tabla User
    @cvar estado: Enum de los tipos de estados por los que puede pasar un proyecto: Pendiente, Aprobada, Rechazada y Ejecutada
    @cvar observaciones: Un campo de texto
    @cvar comite: Relacion muchos a muchos con la tabla User
    """

    solicitud= models.ForeignKey(Solicitud, related_name='solicitud asociada')
  #  usuario = models.ForeignKey(User, related_name='votante')
    estado=models.CharField(max_length=3,choices= ESTADOS, default='PEN')
    observaciones = models.TextField(verbose_name='Observaciones(Opcional)',blank=True)
   # comite = models.ManyToManyField(User, related_name='comite')#una solicitud de cambio tiene varios usuarios miembros de su comite
    # y un user puede estar en varias solicitudes

