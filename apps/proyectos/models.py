__author__ = 'alvarenga'
from django.db import models

class Proyecto(models.Model):
    """
    Modelo Proyecto..
    """
    id = models.IntegerField(default=0,blank=True)
    '''
       id del usuario
    '''
    tipo = models.CharField(max_length=64,blank=True)

    nombre = models.CharField(max_length=64,blank=True)
    '''
       nombre del proyecto
    '''
    Activo = models.BooleanField(null=False)
    '''
       si se encuentra activo o no el proyecto
    '''