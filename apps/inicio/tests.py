'''Created on April 11, 2014
@author: msekatcheff

'''


from django.test import Client, TestCase
from django.contrib.auth.models import User
import unittest





class SIAPTestSuite_it1(unittest.TestCase):
    "Show setup and teardown"

    def setUp(self):
        self.client = Client()
        self.username = 'marcel'
        self.email = 'sekat@gmail.com'
        self.password = '12345'
        self.test_user = User.objects.create_user(self.username, self.email, self.password)
    def tearDown(self):
        self.test_user.delete()



    def test_11(self):
        login = self.client.login(username=self.username, password=self.password)
        return self.assertEqual(login, True)


    def setUp2(self):
        '''Esta prueba debe fallar, datos incorrectos'''
        self.client = Client()
        self.username = 'prueba'

        self.email = 'algo@gmail.com'
        self.password = '12345123'
        self.test_user = User.objects.create_user('username', 'yahoo@yahoo.com', '0987')



    def test_12(self):
        login = self.client.login(username='prueba', password='0987')
        #print(login)
        #login = self.client.login(username='prueba', password='0987')
        return self.assertEquals(login, False)
