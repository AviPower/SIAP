

'''Created on April 11, 2014
@author: msekatcheff

'''


from django.test import Client, TestCase
from django.contrib.auth.models import User
import unittest
from .models import Perfiles




class SIAPTestSuite_it1(TestCase):

    def setUp(self):
        self.client = Client()
        self.usuario = 'marcel'
        self.email = 'sekat@gmail.com'
        self.password = '12345'
        self.test_user = User.objects.create_user(self.usuario, self.email, self.password)



    def test_11(self):
        login = self.client.login(usuario=self.usuario, password=self.password)
        self.assertEqual(login, False)










