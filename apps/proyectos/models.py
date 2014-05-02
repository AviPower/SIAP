__author__ = 'alvarenga'
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
ESTADOS = (

    ('PEN', 'Pendiente'),
    ('ANU','Anulado'),
    ('ACT', 'Activo'),
    ('FIN','Finalizado'),
    ('ELI','Eliminado')
)


class Proyecto(models.Model):

    """
    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar nombre: Cadena de caracteres
    @cvar descripcion: Un campo de texto
    @cvar  fecha_ini: Fecha que indica el inicio de un proyecto
    @cvar fecha_fin: Fecha que indica el fin estimado de un proyecto
    @cvar estado: Enum de los tipos de estados por los que puede pasar un proyecto: Pendiente, Anulado, Activo y Finalizado
    @cvar lider: Clave foranea a la tabla User
    @cvar observaciones: Un campo de texto
    @cvar comite: Relacion muchos a muchos con la tabla User
    """

    nombre= models.CharField(max_length=100, verbose_name='Nombre',unique=True)
    descripcion= models.TextField(verbose_name='Descripcion')
    fecha_ini=models.DateField(null=False)
    fecha_fin=models.DateField(null=False)
    estado=models.CharField(max_length=3,choices= ESTADOS, default='PEN')
    lider = models.ForeignKey(User, related_name='lider')
    observaciones = models.TextField(verbose_name='Observaciones')
    comite = models.ManyToManyField(User, related_name='comite')