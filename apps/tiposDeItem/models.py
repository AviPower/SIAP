__author__ = 'alvarenga'
from django.db import models
from apps.fases.models import Fase
# Create your models here.
TIPOS = (

    ('NUM', 'Numerico'),
    ('TEX','Texto'),
    ('LOG', 'Logico'),
    ('FEC','Fecha')
)

class TipoItem(models.Model):
    """
    Clase del Modelo que representa al tipo de item
    @cvar nombre: Cadena de caracteres
    @cvar descripcion: Un campo de texto
    @cvar fase: Clave foranea a la tabla Fase
    """
    nombre=models.CharField(max_length=100, null=False, verbose_name="Nombre")
    descripcion=models.TextField(max_length=140, null=True, verbose_name="Descripcion")
    fase=models.ForeignKey(Fase, related_name='fase', null=True, verbose_name="Fase")

class Atributo(models.Model):
    """
    Clase del Modelo que representa a un atributo de tipo de item
    @cvar nombre: Cadena de caracteres
    @cvar tipo: Enun de los variaciones de un atributo de tipo de item, puede ser numerico, texto, logico, fecha
    @cvar tipoItem: relacion muchos a muchos con la tabla TipoItem
    """

    nombre=models.CharField(max_length=100, null=Fase, verbose_name="Nombre")
    tipo=models.CharField(max_length=3,choices=TIPOS, default='TEX', verbose_name="Tipo de Dato" )
    valorDefecto=models.CharField(max_length=140, verbose_name="Valor por defecto")
#    tipoItem=models.ForeignKey(TipoItem, related_name='tipoItem', verbose_name="Tipo de Item")
    tipoItem=models.ManyToManyField(TipoItem)

#class AtributoItem(models.Model):
#    id_item=models.SmallIntegerField(null=False);
#    id_atributo=models.SmallIntegerField(null=False);
#    valor=models.CharField(max_length=256);