__author__ = 'teaser'
from django.test import TestCase, Client
from apps.fases.models import Fase
from apps.proyectos.models import Proyecto
from django.contrib.auth.models import User




class FaseTest(TestCase):


    def setUp(self):
        print "\nTEST FASE"

        u4 = User.objects.create(username='avelinaaa', first_name='runJoey', last_name='passit',
                                       password='fija')

        proyecto = Proyecto.objects.create(nombre='prueba', descripcion="Este es un proyecto",
                                           fecha_ini="2014-01-12",
                                           fecha_fin="2014-01-14",
                                           lider= u4,
                                           observaciones="esta es una observacion")

        Fase.objects.create(nombre='faseprueba', descripcion="Este es una fase",
                            maxItems = 3,  fInicio="2014-01-12", orden = 3,
                            fCreacion="2014-01-10", proyecto = proyecto)
        print("Creo la fase mediante el metodo setUp")



    def test_ABMFase(self):
        valido=False
        print "\n----------Se procede a buscar la fase de prueba creada"
        valido = Fase.objects.filter(nombre="faseprueba").exists()
        print ("valido=", valido)
        if valido:
            print "\nSe encontro la fase creada"
        if valido==False:
            print "\n-No se ha creado la fase"
        print "\n----------Ahora se busca una fase que no existe"
        valido=False
        valido=Proyecto.objects.filter(nombre="fasepruebanoexiste").exists()
        if valido==False:
            print "\nNo existe la fase "
        print "\n----------Se procede a buscar la fase creada para modificar su nombre"
        valido = Fase.objects.filter(nombre="faseprueba").exists()
        print ("valido para modificar=", valido)
        if valido:
            print "\nSe encontro la fase y se procedera a cambiar el valor del campo nombre"
            valido = Fase.objects.filter(nombre="faseprueba").update(nombre= "nuevoNombre")
            print ("valido para modificar despues de actualizar=", valido)
            if valido:
                print "\nLa fase fue modificada adecuadamente con nombre= nuevoNombre"

        print "\n----------Se procede a borrar la fase "
       # valido = False
        valido= Fase.objects.filter(nombre="faseprueba").exists()
        fas = Fase.objects.filter(nombre="faseprueba")
        print ("valido=", valido)
        print ("nombre=", dir(fas.values_list()))
        if valido:
                fas = Fase.objects.filter(nombre="faseprueba")
                fas.delete()
                print "\nFase Borrada"
        if valido==False:
             print "Error al borrar la fase, se debe dar un nombre de fase existente"









