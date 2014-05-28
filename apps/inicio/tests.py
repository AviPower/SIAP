# -*- coding: utf-8 -*-
'''Created on April 11, 2014
@author: msekatcheff

'''


from django.test import Client, TestCase
from django.contrib.auth.models import User
import unittest
from django.contrib.auth import SESSION_KEY




class SIAPTestSuite_it1(unittest.TestCase):
    """
    Clase que implementa una suite para los test de Login de Usuario
    """

    def setUp(self):
        """
        Funcion que inicializa el test con Datos de Prueba sobre usuarios
        sobre datos de la BD
        """

        self.client = Client()
        self.username = 'marcel'
        self.email = 'sekat@gmail.com'
        self.password = '12345'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)

    def tearDown(self):
        """
        @param self
        Llamado una vez finalizado el test
        """

        self.test_user.delete()

    def test_11(self):
        """
        Datos Correctos
        @param self
        @return self.assertEqual(login, True)
        """

        login = self.client.login(username=self.username, password=self.password)
        return self.assertEqual(login, True)

    def test_12(self):
        """
        Datos incorrectos sobre la Base de Datos
        @param self
        @return self.assertEquals(login, False)
        """

        login = self.client.login(username='prueba', password='0987')
        return self.assertEquals(login, False)

    def test_inicio(self):
        '''Test para ver si puede entrar a la pagina de inicio'''
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def logout(self):
        '''
        Test para el logout
        '''
        usuario = User.objects.create_user('testuser', 'test@example.com', 'testpw')
        c = Client()
        c.login(username='tesuser', password='testpw')
        response = c.get('/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(SESSION_KEY not in self.client.session)

from .forms import UserForm
from .models import Perfiles

class UserFormTestCase(TestCase):

    def test_valid_form(self):

        user = User.objects.create(username='avi',first_name='avelina',last_name='alvarenga',email='avi@avi.com')
        perfil=Perfiles()
        perfil.usuario=user
        perfil.telefono='083472'
        perfil.direccion='Asuncion'
        perfil.lider='False'
        data = {
            'name':'Asuncion',

        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form(self):
        "perfil requiere campo para validar"
        data = {
            'perfil_0': 'Foo',
            'perfil_1': '',
        }
        form = UserForm(data=data)
        self.assertFalse(form.is_valid())