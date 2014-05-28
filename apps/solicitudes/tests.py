# -*- coding: utf-8 -*-
from lib2to3.fixer_util import p1

__author__ = 'marcel'

from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.inicio.models import Perfiles
from apps.solicitudes.models import Solicitud



class SolicitudTest(TestCase):


    def setUp(self):
        print "\n-----------------TEST SOLICITUD DE CAMBIO------------------------------"

        Solicitud.objects.create(nombre='solici', descripcion="Esta es una solicitud",
                                           fecha_solicitud="2014-01-12")

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




