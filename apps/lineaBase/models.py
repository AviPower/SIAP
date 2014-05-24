__author__ = 'alvarenga'
from django.db import models
from apps.fases.models import Fase

# Create your models here.
class LineaBase(models.Model):
    """
    Se crea el modelo Linea Base

    Estan definidos en la tabla los atributos

    - nombre: Nombre de la linea base
    - estado: puede encontrarse en 2 estados: Abierta y Cerrada.
    - id_fase: el id de la Fase a la que pertenece
    """
    estados_probables= (
        ('C','Cerrada'),
        ('A','Abierta'),
    )
    nombre= models.CharField(max_length=50, null=False)
    estado= models.CharField ( max_length = 1 ,  choices = estados_probables, default='A')
    fase=models.ForeignKey(Fase)
    activo= models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre