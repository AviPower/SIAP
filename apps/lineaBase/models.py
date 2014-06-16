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
    ESTADOS = (
    ('CERRADA','Cerrada'),
    ('ROTA','Rota'),

)
    nombre= models.CharField(max_length=100, null=False)
    estado=models.CharField(max_length=8, verbose_name='Estado',choices=ESTADOS)
    fase=models.ForeignKey(Fase)
    activo= models.BooleanField(default=True)

    def __unicode__(self):
        return self.nombre
