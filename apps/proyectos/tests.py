# -*- coding: utf-8 -*-
from lib2to3.fixer_util import p1

__author__ = 'alvarenga'

from django.test import TestCase, Client
from django.contrib.auth.models import User
from apps.inicio.models import Perfiles
from apps.proyectos.models import Proyecto

# Create your tests here.
class SIAPTestCase(TestCase):
    fixtures = ["proyectos_testmaker"]

    def test_buscar_proyectos(self):
        '''
        Test para buscar un proyecto
        '''
        c = Client()
        print "\n\n-------------------Buscando Proyectos-----"
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/proyectos/search/?q=SIAP33')
        print "Status 200, indica exito\n"
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.nombre for proyecto in resp.context['datos']], ['SIAP33'])


    def test_detalle_proyectos(self):
        '''
        Test para visualizar los detalles de un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        print "\n--------Listando los detalles de un proyecto-------"
        #Test para proyecto existente
        resp = c.get('/proyectos/1')
        self.assertEqual(resp.status_code, 200)
        print "Status 200, indica exito\n"
        self.assertEqual(resp.context['proyecto'].pk, 1)
        self.assertEqual(resp.context['proyecto'].nombre, 'SIAP')

        #Test para proyecto inexistente
        print "\nMostrando un proyecto inexistente\n"
        resp = c.get('/proyectos/1000')
        self.assertEqual(resp.status_code, 404)

    def test_listar_proyectos(self):
        '''
         Test para ver si lista correctamente un proyecto
        '''
        print "\n\n--------Listando los proyectos-------"
        c = Client()
        c.login(username='admin', password='admin')
        #proyecto= Proyecto.objects.create(id=3, nombre='pruebaProyecto',descripcion='prueba',observaciones='prueba',fecha_ini='2012-12-01',fecha_fin='2013-12-01',lider_id=1)
        resp = c.get('/proyectos/')
        self.assertEqual(resp.status_code, 200)
        print "Status 200, indica exito\n"
        self.assertEqual([proyecto.pk for proyecto in resp.context['datos']], [1, 2, 3, 4, 5, 6, 7])

    def test_ver_equipo(self):
        '''
         Test para ver si lista correctamente los usuarios asociados a un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        print "\n----------Verifica si la url de visualizar el equipo de trabajo realiza correctamente su operacion"
        resp = c.get('/proyectos/equipo/1')
        self.assertEqual(resp.status_code, 200)
        print "\nStatus 200, indica exito\n"
        self.assertEqual([lider.pk for lider in resp.context['comite']], [10, 19, 1])

    def test_modficar_proyecto(self):
        '''
         Test para ver si modifica correctamente un proyecto
        '''
        c = Client()
        print "\n\n--------Se intenta modificar los proyectos-------"
        c.login(username='admin', password='admin')
        #test para verificar que si no modifica nada, no guarda
        resp = c.post('/proyectos/modificar/1')
        self.assertEqual(resp.status_code, 200)
        print "Status 200, indica exito, se redirige adecuadamente\n"


    def test_importar(self):
        '''
         Test para ver si importa correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        #prueba importar un proyecto y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe un proyecto con ese nombre
        resp = c.post('/proyectos/importar/1', {'nombre': 'SIAP'})

        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)

    def test_registrar(self):
        '''
         Test para ver si crea correctamente un proyecto
        '''

        c = Client()
        c.login(username='admin', password='admin')
        print "-------------------Creando Proyectos-----"
        #prueba importar un proyecto y asignarle como nombre un nombre ya existente. Retorna un mensaje de nivel 20,
        #informando que ya existe un proyecto con ese nombre
        resp = c.post('/proyectos/registrar/', {'nombre': 'SIAP'})
        print "Crea correctamente el proyecto,  llena el formulario de la url /proyectos/registrar/ mediante el cual llama al metodo 'crear_rol' que recibe el request"
        self.assertEqual(resp.status_code, 200)

        self.assertEqual(resp.context['messages'].level, 20)

        #registra correctamente y redirige a la pagina indicada
        resp = c.post('/proyectos/registrar/',
                      {'nombre': 'Proyecto nuevo', 'descripcion': 'ds', 'observaciones': 'sdasd',
                       'fecha_ini': '20/02/2014', 'fecha_fin': '20/02/2015', 'lider': 1, 'comite': 1}, follow=True)
        self.assertEqual(resp.status_code, 200)
        #self.assertRedirects(resp, 'http://testserver/proyectos/register/success/')
        print "Status 200, indica exito en la operacion\n"
        #no registra correctamente ya que la fecha de inicio es despues de la de fin
        resp = c.post('/proyectos/registrar/',
                      {'nombre': 'Proyecto nuevo 2', 'descripcion': 'ds', 'observaciones': 'sdasd',
                       'fecha_ini': '20/02/2015', 'fecha_fin': '20/02/2014', 'lider': 1, 'comite': 1})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['messages'].level, 20)



class ProyectoTest(TestCase):


    def setUp(self):
        print "\n-----------------TEST PROYECTO------------------------------"

        u4 = User.objects.create(username='avelinaaa', first_name='runJoey', last_name='passit',
                                       password='fija')

        Proyecto.objects.create(nombre='prueba', descripcion="Este es un proyecto",
                                           fecha_ini="2014-01-12",
                                           fecha_fin="2014-01-14",
                                           lider= u4,
                                           observaciones="esta es una observacion")
                                           #comite=crear_comite([u2, u3])
        print("Creo el proyecto mediante el metodo setUp()")





    def test_ABMProyecto(self):
        valido=False

        valido = Proyecto.objects.filter(nombre="prueba").exists()
        if valido:
            print "\nSe encontro el Proyecto creado"
        if valido==False:
            print "\n-No se ha creado el proyecto"
        print "\n----------Ahora se busca un proyecto que no existe"
        valido=False
        valido=Proyecto.objects.filter(nombre="pruebanoexiste").exists()
        if valido==False:
            print "\nNo existe el proyecto "
        print "\n----------Se procede a buscar el Proyecto creado para modificar su nombre"
        valido = Proyecto.objects.filter(nombre="prueba").exists()
        if valido:
            print "\nSe encontro el Proyecto creado y se procedera a cambiar el valor del campo nombre"
            valido = Proyecto.objects.filter(nombre="prueba").update(nombre= "nombreCambiado")
            if valido:
                print "\nEl proyecto fue modificado adecuadamente con nombre= nombreCambiado"

        print "\n----------Se procede a borrar el proyecto "
        valido = False
        valido= Proyecto.objects.filter(nombre="nombresCambiado").exists()
        if valido:
                pro = Proyecto.objects.filter(nombre="nombresCambiado")
                pro.delete()
                print "\nProyecto Borrado"
        if valido==False:
             print "Error al borrar el proyecto, se debe dar un nombre de uno existente"




