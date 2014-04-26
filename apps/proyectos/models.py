__author__ = 'alvarenga'
from django.db import models

class Proyecto(models.Model):
    """
    Modelo Proyecto..
    """
    id = models.IntegerField(default=0,blank=True)
    '''
       telefono es numero telefonico perteneciente al usuario
    '''
    tipo = models.CharField(max_length=64,blank=True)

    nombre = models.CharField(max_length=64,blank=True)
    '''
       direccion es direccion en la cual reside el usuario
    '''
    Activo = models.BooleanField(null=False)
    '''
       representa si el usuario en cuestion es lider o no
    '''