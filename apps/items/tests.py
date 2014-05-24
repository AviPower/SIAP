# -*- coding: utf-8 -*-
__author__ = 'teaser'
from apps.items.models import Item
from django.test import TestCase
from apps.tiposDeItem.models import TipoItem

class ItemTestCase (TestCase):
    def setUp (self):
        tipoIt =TipoItem.objects.create(nombre="detalles", descripcion="aa")
        print "\n -------------------TEST ITEM----------"
        print "\n Se crear un Item"
        print "\n Buscar el Item creado"
        Item.objects.create(nombre="itemprueba", descripcion="aa", costo =3, tiempo= 3,
                            estado= 'PEN', version= 1, fecha_creacion = '2014-05-12', fecha_mod= '2014-05-15',
                            tipo_item = tipoIt
                            )

    def test_ABMItems(self):
        valido=False

        valido = Item.objects.filter(nombre="itemprueba").exists()
        if valido:
            print "\nSe encontro el item creado"
        if valido==False:
            print "\nNo se ha creado el item"
        print "\n----------Ahora se busca un proyecto que no existe"
        valido=False
        valido=Item.objects.filter(nombre="itemprueba").exists()
        if valido==False:
            print "\nNo existe el item "
        print "\n----------Se procede a buscar el item creado para modificar su nombre"
        valido = Item.objects.filter(nombre="itemprueba").exists()
        if valido:
            print "\nSe encontro el item creado y se procedera a cambiar el valor del campo nombre"
            valido = Item.objects.filter(nombre="itemprueba").update(nombre= "nombreitemCambiado")
            if valido:
                print "\nEl item fue modificado adecuadamente con nombre= nombreitemCambiado"

        print "\n----------Se procede a borrar el item "
        valido = False
        valido= Item.objects.filter(nombre="nombreitemCambiado").exists()
        if valido:
                item = Item.objects.filter(nombre="nombreitemCambiado")
                item.delete()
                print "\nItem Borrado"
        if valido==False:
             print "Error al borrar el item, se debe dar un nombre de uno existente"




