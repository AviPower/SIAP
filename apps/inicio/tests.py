# coding=utf-8
'''Created on April 11, 2014
@author: msekatcheff

'''


from django.test import Client, TestCase
from django.contrib.auth.models import User
import unittest





class SIAPTestSuite_it1(unittest.TestCase):
    """
    Clase que implementa una suite para los test de Login de Usuario
    """

    def setUp(self):
        """
        Función que inicializa el test con Datos de Prueba sobre usuarios
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
