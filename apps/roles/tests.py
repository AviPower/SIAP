# -*- coding: utf-8 -*-
__author__ = 'alvarenga'
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import Group

class SIAPTestCase(TestCase):

    fixtures = ["fases_testmaker"]

    def test_crear_rol(self):
        '''
        Test para la creacion de un rol
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        print "-------------------Creando Roles-----"
        #creacion correcta del rol, redirige a la pagina correspondiente

        print "Crea correctamente el rol Llena el formulario de la url /roles/crear/ mediante el cual llama al metodo crear_rol que recibe el request"
        resp = c.post('/roles/crear/',{'name':"Rol 1"},follow=True)
        self.assertEqual(resp.status_code,200)
        print "Status 200, indica exito\n"
 #      self.assertRedirects(resp, 'http://testserver/roles/register/success/')

        #creacion incorrecta: nombre repetido, no redirige
        resp = c.post('/roles/crear/',{'name':"Rol 1"})
        self.assertEqual(resp.status_code,200)


    def test_listar_roles(self):
        '''
         Test para crear un rol y ver si lo lista correctamente
        '''
        c = Client()
        print "-----Listando los roles para el usuario de prueba admin-----"
        c.login(username='admin', password='admin1')
        resp = c.get('/roles/')
        print "Codigo 200 indica exito\n"
        self.assertEqual(resp.status_code, 200)

    def test_detalle(self):
        '''
         Test para crear un rol y ver si lo lista correctamente
        '''
        print "--------Listando los detalles de un rol-------"
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_rol()
        #ver detalle de un rol existente
        resp = c.get('/roles/3')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['rol'].pk, 3)
        print "Comprobando que el nombre del rol es Analista de la Fase 1\n"
        self.assertEqual(resp.context['rol'].name, 'Analista de la Fase 1')
        #ver detalle de un rol inexistente
        resp = c.get('/roles/100')
        boolu=False
        boolu =self.assertEqual(resp.status_code, 404)
        if boolu:
            print "Si se imprime esto es que se trato de ver detalle \n"

    def test_eliminar(self):
        '''
         Test para crear un rol y ver si lo lista correctamente
        '''
        boolu2=False
        print "--------Se muestran el exito de la operacion eliminar un rol del usuario de prueba admin-----------"
        c = Client()
        c.login(username='admin', password='admin1')
        self.test_crear_rol()
        #eliminacion de un rol existente
        resp = c.get('/roles/eliminar/4')
        boolu2 = self.assertEqual(resp.status_code, 200)
        if boolu2:
            print "Codigo 200 indica exito"
        #eliminacion de un rol inexistente, (ya se borro)
        resp = c.get('/roles/eliminar/56')
        boolu2 = self.assertEqual(resp.status_code, 404)
        if boolu2:
            print "Codigo 404 indica exito, indica que no se encontro ese rol"


    def test_modificar_rol(self):
        '''
        Test para la modificacion de un rol
        '''
        c = Client()
        c.login(username='admin', password='admin1')
        bool3 = False
        print "--- Verificando validez de las url para modificar roles-----"
        #modificacion correcta del rol, redirige a la pagina correspondiente
        print "Primero se crea"
        resp = c.post('/roles/crear/',{'name':"Rol 1"})
        print "Luego se modifica"
        resp = c.post('/roles/modificar/5',{'name':"Rol 4"},follow=True)
        bool3 = self.assertEqual(resp.status_code, 200)
        if bool3:
            print "Si llego aqui redirige adecuadamente"
        self.assertRedirects(resp, 'http://testserver/roles/register/success/')
        #modificacion incorrecta, no redirige, ya que el nombre de la fase ya existe
        resp = c.post('/roles/crear/',{'name':"Rol 1"})
        resp = c.post('/roles/modificar/5',{'name':"Rol 1"})
        self.assertEqual(resp.status_code, 200)


    def test_buscar_roles(self):
        '''
        Test para buscar un rol
        '''
        boole5 = False
        c = Client()
        print "Se procede a buscar roles"
        c.login(username='admin', password='admin1')
        #Test para  buscar rol existente
        resp = c.post('/roles/crear/',{'name':"Rol1"})
        resp = c.get('/roles/search/?q=Rol1')
        print "Codigo 200, indica exito"
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.name for proyecto in resp.context['datos']], ['Rol1'])

        #test para buscar un rol inexistente,no encuentra ningun rol
        resp = c.get('/roles/search/?q=noexiste')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual([proyecto.name for proyecto in resp.context['datos']], [])


