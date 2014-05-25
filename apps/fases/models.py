# -*- coding: utf-8 -*-

__author__ = 'alvarenga'
from django.db import models
from django.contrib.auth.models import Group
from apps.proyectos.models import Proyecto

# Create your models here.

ESTADOS = (

    ('PEN','Pendiente'),
    ('DES','Desarrollo'),
    ('COMPL','Completa'),
    ('COMPR','Comprometida'),
)
# usar get_estado_display()

class Fase(models.Model):
    """
    Modelo que representa a una Fase con sus atributos
    @cvar nombre: Cadena de caracteres
    @cvar descripcion: Un campo de texto
    @cvar posicion: Entero corto que indica su posicion relativa de la fase entre 1 y la cantidad de fases que posee el proyecto
    @cvar maxItems: Entero corto que representa la cantidad de items
    @cvar fInicio: Fecha que indica el inicio
    @cvar fFin: Fecha que indica el posible finalizacion
    @cvar orden: Entero corto que representa el orden relative de items
    @cvar estado: Enum de los tipos de estados por los que puede pasar una fase: Pendiente, Desarrollo, Completa y Comprometida
    @cvar fCreacion: Fecha que indica el instante en que se crea la fase
    @cvar roles: relacion muchos a muchos con la tabla de Grupos
    @cvar proyecto: clave foranea a proyecto
    """
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    descripcion = models.TextField(verbose_name='Descripcion')
    maxItems = models.SmallIntegerField(verbose_name='Cantidad max de Items')
    #posicion = models.SmallIntegerField(verbose_name='Posicion relativa de la fase dentro del proyecto')
    fInicio = models.DateField(verbose_name='Fecha de Inicio, formato  DD/MM/AAAA')
   # fFin = models.DateField(verbose_name='Fecha de Finalizacion')
    orden = models.SmallIntegerField(verbose_name='Orden')
    estado = models.CharField(max_length=3, choices=ESTADOS, verbose_name='Estado')
    fCreacion = models.DateField(verbose_name='Fecha de Creacion', auto_now=True)
#    fModificacion = models.DateField(verbose_name='Fecha de Modificacion')
    roles = models.ManyToManyField(Group)
    proyecto = models.ForeignKey(Proyecto)
