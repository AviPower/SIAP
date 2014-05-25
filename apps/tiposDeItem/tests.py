# -*- coding: utf-8 -*-
from django.test import TestCase
from apps.tiposDeItem.models import TipoItem



class TipoItemTestCase (TestCase):
    def setUp (self):
        print "\n TEST TIPOITEM"
        print "\n --Se crear un TipoItem de nombre detalles"
        print "\n --Buscar el TipoItem creado"
        TipoItem.objects.create(nombre="detalles", descripcion="aa")

    def test_TipoItemtraer(self):
        valido = False
        valido = TipoItem.objects.filter(nombre="detalles").exists()
        if valido:
            print "\n---Se ha encontrado el TipoItem creado"
        if valido==False:
            print "\n---No se ha creado el TipoItem"
        print "\n --Buscar un TipoItem inexistente"
        valido = False
        valido = TipoItem.objects.filter(nombre="detallesExtras").exists()
        if valido==False:
            print "\n---No existe el TipoItem buscado"
