# -*- coding: utf-8 -*-
from lib2to3.fixer_util import p1

__author__ = 'marcel'

from django.test import TestCase, Client
from apps.solicitudes.models import Solicitud
from apps.fases.models import Fase
from apps.proyectos.models import Proyecto
from django.contrib.auth.models import User
from apps.items.models import Item
from apps.tiposDeItem.models import TipoItem


class SolicitudTest(TestCase):


    def setUp(self):
        print "\n-----------------TEST SOLICITUD DE CAMBIO------------------------------"
        user = User.objects.create(username='avelinaaa', first_name='runJoey', last_name='passit',
                                       password='fija')

        proyecto = Proyecto.objects.create(nombre='prueba', descripcion="Este es un proyecto",
                                           fecha_ini="2014-01-12",
                                           fecha_fin="2014-01-14",
                                           lider= user,
                                           observaciones="esta es una observacion")

        faseprueba = Fase.objects.create(nombre='faseprueba', descripcion="Este es una fase",
                            maxItems = 3,  fInicio="2014-01-12", orden = 3,
                            fCreacion="2014-01-10", proyecto = proyecto)
        faseprueba.save()


        tipoIt =TipoItem.objects.create(nombre="detalles", descripcion="aa")
        item = Item.objects.create(nombre="itemprueba", descripcion="aa", costo =3, tiempo= 3,
                            estado= 'PEN', version= 1, fecha_creacion = '2014-05-12', fecha_mod= '2014-05-15',
                            tipo_item = tipoIt, fase = faseprueba
                            )


        Solicitud.objects.create(nombre='solici', descripcion="Esta es una solicitud",
                                           fecha="2014-01-12", proyecto = proyecto, item = item,
                                           costo = 3, tiempo = 4, usuario = user)

        print("Creo la solicitud  mediante el metodo setUp()")





    def test_ABMSolicitud(self):
        valido=False

        valido = Solicitud.objects.filter(nombre="solici").exists()
        if valido:
            print "\nSe encontro la solicitud creada"
        if valido==False:
            print "\n-No se ha creado la solicitud"
        print "\n----------Ahora se busca una solicitud que no existe"
        valido=False
        valido=Solicitud.objects.filter(nombre="pruebanoexiste").exists()
        if valido==False:
            print "\nNo existe la solicitud "
        print "\n----------Se procede a buscar la solicitud creada para modificar su nombre"
        valido = Solicitud.objects.filter(nombre="solici").exists()
        if valido:
            print "\nSe encontro el Proyecto creado y se procedera a cambiar el valor del campo nombre"
            valido = Solicitud.objects.filter(nombre="solici").update(nombre= "soliciCambiado")
            if valido:
                print "\nLa solicitud fue modificada adecuadamente con nombre= soliciCambiado"




