# -*- coding: utf-8 -*-
from lib2to3.fixer_util import p1

__author__ = 'marcel'

from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.inicio.models import Perfiles
from apps.lineaBase.models import LineaBase
from apps.proyectos.models import Proyecto
from apps.fases.models import Fase


class LBTest(TestCase):


    def setUp(self):
        print "\n-----------------TEST SOLICITUD DE CAMBIO------------------------------"

        u4 = User.objects.create(username='avelinaaa', first_name='runJoey', last_name='passit',
                                       password='fija')

        proyecto = Proyecto.objects.create(nombre='prueba', descripcion="Este es un proyecto",
                                           fecha_ini="2014-01-12",
                                           fecha_fin="2014-01-14",
                                           lider= u4,
                                           observaciones="esta es una observacion")

        faseprueba = Fase.objects.create(nombre='faseprueba', descripcion="Este es una fase",
                            maxItems = 3,  fInicio="2014-01-12", orden = 3,
                            fCreacion="2014-01-10", proyecto = proyecto)

        LineaBase.objects.create(nombre='lbprueba',estado = 'A', fase = faseprueba, activo = True)

        print("Creo la solicitud  mediante el metodo setUp()")





    def test_ABMLB(self):
        valido=False

        valido = LineaBase.objects.filter(nombre="lbprueba").exists()
        if valido:
            print "\nSe encontro la linea de base creada"
        if valido==False:
            print "\n-No se ha creado la linea de base"
        print "\n----------Ahora se busca una linea de base que no existe"
        valido=False
        valido=LineaBase.objects.filter(nombre="lbprueba").exists()
        if valido==False:
            print "\nNo existe la linea de base "
        print "\n----------Se procede a buscar la linea de base creada para modificar su nombre"
        valido = LineaBase.objects.filter(nombre="lbprueba").exists()
        if valido:
            print "\nSe encontro la linea de base creada y se procedera a cambiar el valor del campo nombre"
            valido = LineaBase.objects.filter(nombre="lbprueba").update(nombre= "lbpruebacambiado")
            if valido:
                print "\nLa solicitud fue modificada adecuadamente con nombre= lbpruebacambiado"

        print "\n----------Se procede a borrar la linea Base"
        valido = False
        valido= LineaBase.objects.filter(nombre="lbpruebacambiado").exists()
        if valido:
                pro = Proyecto.objects.filter(nombre="lbpruebacambiadosss")
                pro.delete()
                print "\nLinea Base Borrada"
        if valido==False:
             print "Error al borrar la linea base, se debe dar un nombre de uno existente"







