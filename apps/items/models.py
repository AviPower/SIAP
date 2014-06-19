from django.db import models
from django.contrib.auth.models import Group
from apps.tiposDeItem.models import TipoItem, Atributo
from apps.fases.models import Fase
from apps.lineaBase.models import LineaBase

# Create your models here.
ESTADOS = (
    ('PEN','Pendiente'),#abierta
    ('CON','En Construccion'),#desarrollo
    ('FIN','Finalizado'),#cerrado cuando en una linea base
    ('VAL','Validado'),#iniciado o aprobado
    ('REV','Revision'),#revisar
    ('ANU','Anulado'),#inactivo
    ('BLO','Bloqueado')
)
TIPOS = (

    ('Padre', 'Padre'),
    ('Antecesor', 'Padre'),

)
class Item(models.Model):
    """
    Modelo que representa a un Item
    @cvar nombre: Cadena de caracteres
    @cvar descripcion: Un campo de texto
    @cvar costo: Entero positivo que representa el costo del item
    @cvar tiempo: Entero positivo que representa la cantidad de tiempo en dias
    @cvar estado: Enum de los tipos de estados por los que puede pasar una fase: Pendiente, En Construccion, Finalizado, Validado, Revision, Anulado
    @cvar version: Entero corto con valores positivos
    @cvar orden: Entero corto que representa el orden relative de items
    @cvar relacion: clave foranea a otro item
    @cvar tipo: Enum de los tipos de relaciones entre items: Padre-Padre-Antecesor-Padre
    @cvar fecha_creacion: Tipo de dato Date
    @cvar fecha_mod: Tipo de dato Date
    @cvar tipo_item: clave foranea a tipo item
    """
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    version=models.PositiveSmallIntegerField(verbose_name='Version')
    relacion=models.ForeignKey('self',null=True, verbose_name='Relacion', related_name='relacionItem')
    tipo=models.CharField(null=True,max_length=10, choices=TIPOS, verbose_name='Tipo')
    fecha_creacion=models.DateField(verbose_name='Fecha de Creacion')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    tipo_item=models.ForeignKey(TipoItem)
    fase=models.ForeignKey(Fase)
    lineaBase=models.ForeignKey(LineaBase, null=True)

class VersionItem(models.Model):
    """
    Modelo que representa a una Version de Item
    @cvar id_item: Clave foranea a item
    @cvar nombre: Campo de texto
    @cvar descripcion: Un campo de texto
    @cvar costo: Entero positivo que representa el costo del item
    @cvar tiempo: Entero positivo que representa la cantidad de tiempo en dias
    @cvar estado: Enum de los tipos de estados por los que puede pasar una fase: Pendiente, En Construccion, Finalizado, Validado, Revision, Anulado
    @cvar version: Entero corto con valores positivos
    @cvar relacion: clave foranea a otro item
    @cvar tipo: Enum de los tipos de relaciones entre items: Padre-Padre-Antecesor-Padre
    @cvar fecha_creacion: Tipo de dato Date
    @cvar fecha_mod: Tipo de dato Date
    @cvar tipo_item: clave foranea a tipo item
    """
    id_item=models.ForeignKey(Item, verbose_name='Item', related_name='itemVersion')
    nombre=models.CharField(max_length=100, verbose_name='Nombre')
    descripcion=models.TextField(max_length=140, verbose_name='Descripcion')
    costo=models.PositiveIntegerField(verbose_name='Costo')
    tiempo=models.PositiveIntegerField(verbose_name='Tiempo')
    estado=models.CharField(max_length=3,choices=ESTADOS, verbose_name='Estado')
    version=models.PositiveSmallIntegerField(verbose_name='Version')
    relacion=models.ForeignKey(Item,null=True, verbose_name='Relacion',related_name='relacionVersion')
    tipo=models.CharField(null=True,max_length=10, choices=TIPOS, verbose_name='Tipo')
    fecha_mod=models.DateField(verbose_name='Fecha de Modificacion')
    tipo_item=models.ForeignKey(TipoItem)
    fase=models.ForeignKey(Fase)
    lineaBase=models.ForeignKey(LineaBase, null=True)

class Archivo(models.Model):
    """
    Modelo que representa a un Archivo
    @cvar archivo: Campo de tipo Archivo
    @cvar id_item: Clave foranea a Item
    @cvar nombre: Un campo de texto
    """
    archivo=models.FileField(upload_to='archivos')
    id_item=models.ForeignKey(Item, null=True)
    nombre=models.CharField(max_length=100, null=True)

class AtributoItem(models.Model):
    """
    Modelo que representa a un atributo de item
    @cvar archivo: Campo de tipo Archivo
    @cvar id_item: Clave foranea a Item
    @cvar nombre: Un campo de texto
    """
    id_item=models.ForeignKey(Item, verbose_name='Item')
    id_atributo=models.ForeignKey(Atributo, verbose_name='Atributo')
    valor=models.CharField(max_length=100, verbose_name='Valor')
    version=models.PositiveSmallIntegerField(verbose_name='Version')

class VersionAtributoItem(models.Model):
    """
    Modelo que representa a una Version de Atributo de Item
    @cvar id_atributo_item: clave foranea a AtributoItem
    @cvar id_item: Clave foranea a Item
    @cvar id_atributo: Clave foranea a Atributo
    @cvar valor: campo de texto
    @cvar version: entero corto positivo
    """
    id_atributo_item=models.ForeignKey(AtributoItem, verbose_name='Atributo Item')
    id_item=models.ForeignKey(Item, verbose_name='Item')
    id_atributo=models.ForeignKey(Atributo, verbose_name='Atributo')
    valor=models.CharField(max_length=100, verbose_name='Valor')
    version=models.PositiveSmallIntegerField(verbose_name='Version')
