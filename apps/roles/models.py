__author__ = 'alvarenga'
from apps.items.models import Item
from apps.tiposDeItem.models import TipoItem
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
# Create your models here.

#Creamos mas permisos para el modelo Item "Atencion el codigo de abajo solo se debe ejecutar una vez
content_ty = ContentType.objects.get_for_model(Item)
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