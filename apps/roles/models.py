__author__ = 'alvarenga'

from django.db import models
from django.contrib.auth.models import User
from apps.proyectos.models import Proyecto

# Create your models here.
class Rol(models.Model):
    """
    Clase del Modelo que representa al proyecto con sus atributos.
    @cvar nombre: Cadena de caracteres
    @cvar usuario: Clave foranea a la tabla User
    @cvar proyecto: Clave foranea a la tabla Proyecto
    @cvar crear_item: Campo booelano
    @cvar editar_item: Campo booelano
    @cvar consultar_items: Campo booelano
    @cvar establecer_relacion: Campo booelano
    @cvar eliminar_relacion: Campo booelano
    @cvar aprobar_item: Campo booelano
    @cvar revivir_item: Campo booelano
    @cvar reversionar_item: Campo booelano
    @cvar agregar_atributo: Campo booelano
    @cvar eliminar_atributo: Campo booelano
    @cvar completar_atributos: Campo booelano
    @cvar consultar_atributos: Campo booelano
    @cvar crear_tipodeitem: Campo booelano
    @cvar modificar_tipodeitem: Campo booelano
    @cvar eliminar_tipodeitem: Campo booelano
    """
    nombre= models.CharField(max_length=50)
    usuario= models.ForeignKey(User)                             # El usuario que tiene dicho rol
    proyecto= models.ForeignKey(Proyecto, null=True)                # A que proyecto se asocia dicho rol
    #Permisos
    crear_item= models.BooleanField(default=False,verbose_name='Crear Item')
    editar_item= models.BooleanField(default=False,verbose_name='Editar Item')
    consultar_items= models.BooleanField(default=False,verbose_name='Consultar Item')
    establecer_relacion= models.BooleanField(default=False,verbose_name='Establecer Relacion')
    eliminar_relacion= models.BooleanField(default=False,verbose_name='Eliminar Relacion')
    aprobar_item= models.BooleanField(default=False,verbose_name='aprobar item')
    revivir_item= models.BooleanField(default=False,verbose_name='Revivir Item')
    reversionar_item= models.BooleanField(default=False,verbose_name='Reversionar Item')
    #consultar_relaciones= models.BooleanField(default=False,verbose_name='consultar Relaciones')

    agregar_atributo= models.BooleanField(default=False,verbose_name='Agregar Atributo')
    eliminar_atributo= models.BooleanField(default=False, verbose_name='Eliminar Atributo')
    completar_atributos= models.BooleanField(default=False, verbose_name='Editar_atributos')
    consultar_atributos= models.BooleanField(default=False,verbose_name='Consultar Atributos')
    crear_tipodeitem= models.BooleanField(default=False,verbose_name='Crear Tipo Item')
    modificar_tipodeitem= models.BooleanField(default=False, verbose_name='Modificar Tipo Item')
    eliminar_tipodeitem= models.BooleanField(default=False, verbose_name='Eliminar Tipo Item')
    #crear_lineabase= models.BooleanField(default=False)             # - Permisos de Administracion de Lineas Base


    def __unicode__(self):
        return self.nombre


from apps.items.models import Item
from apps.tiposDeItem.models import TipoItem
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.

#Creamos mas permisos para el modelo Item "Atencion el codigo de abajo solo se debe ejecutar una vez
#content_ty = ContentType.objects.get_for_model(Item)
#Permission.objects.create(codename='crear_item',
 #                                     name='Se puede crear item',
  #                                    content_type=content_ty)
#Permission.objects.create(codename='editar_item',
 #                                     name='Se puede editar item',
  #                                    content_type=content_ty)
#Permission.objects.create(codename='eliminar_item',
 #                                     name='Se puede eliminar item',
  #                                     content_type=content_ty)
#Permission.objects.create(codename='aprobar_item',
 #                                     name='Se puede aprobar item',
  #                                    content_type=content_ty)
#Permission.objects.create(codename='revivir_item',
 #                                     name='Se puede revivir item',
  #                                    content_type=content_ty)
#Permission.objects.create(codename='reversionar_item',
 #                                     name='Se puede reversionar item',
  #                                     content_type=content_ty)
#content_ty = ContentType.objects.get_for_model(TipoItem)
#Permission.objects.create(codename='crear_tipoitem',
 #                                     name='Se puede crear tipo item',
  #                                    content_type=content_ty)
#Permission.objects.create(codename='editar_tipoitem',
 #                                     name='Se puede editar tipo item',
  #                                    content_type=content_ty)
#Permission.objects.create(codename='eliminar_tipoitem',
 #                                     name='Se puede eliminar tipo item',
  #                                     content_type=content_ty)