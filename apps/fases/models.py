__author__ = 'alvarenga'
from django.db import models
from django.contrib.auth.models import Group
from apps.proyectos.models import Proyecto

# Create your models here.

ESTADOS = (

    ('PEN','Pendiente'),
    ('EJE','En Ejecucion'),
    ('FIN','Finalizado'),
)
# usar get_estado_display()

class Fase(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', unique=True)
    descripcion = models.TextField(verbose_name='Descripcion')
    maxItems = models.SmallIntegerField(verbose_name='Cantidad max de Items')
    fInicio = models.DateField(verbose_name='Fecha de Inicio')
    orden = models.SmallIntegerField(verbose_name='Orden')
    estado = models.CharField(max_length=3, choices=ESTADOS, verbose_name='Estado')
    fCreacion = models.DateField(verbose_name='Fecha de Creacion', auto_now=True)
#    fModificacion = models.DateField(verbose_name='Fecha de Modificacion')
    roles = models.ManyToManyField(Group)
    proyecto = models.ForeignKey(Proyecto)