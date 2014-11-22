__author__ = 'alvarenga'
from django.test import TestCase, Client

class SIAPTestCase(TestCase):
    '''
    Clase que implementa las distintas pruebas para los distintos reportes que genera el sistema
    '''

    fixtures = ["items_testmaker"]


    def test_reporte_usuarios(self):
        '''
        Test para descargar el reporte de usuarios del sistema
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/reportes/usuarios/')
        self.assertEqual(resp.status_code, 200)
        print 'Reporte de usuarios con permisos de administrador'
        c.login(username='juani', password='12345')
        #Test para proyecto buscar existente
        resp = c.get('/reportes/usuarios/')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de usuarios sin permisos de administrador'

    def test_reporte_roles(self):
        '''
        Test para generar el reporte de roles del sistema
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/reportes/roles/')
        self.assertEqual(resp.status_code, 200)
        print 'Reporte de roles con permisos de administrador'
        c.login(username='juani', password='12345')
        #Test para proyecto buscar existente
        resp = c.get('/reportes/roles/')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de roles sin permisos de administrador'

    def test_reporte_proyectos(self):
        '''
        Test para generar el reporte de proyectos del sistema
        '''
        c = Client()
        c.login(username='admin', password='admin')
        #Test para proyecto buscar existente
        resp = c.get('/reporte/proyectos/')
        self.assertEqual(resp.status_code, 200)
        print 'Reporte de proyectos con permisos de administrador'
        c.login(username='juani', password='12345')
        #Test para proyecto buscar existente
        resp = c.get('/reportes/proyectos/')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de proyectos sin permisos de administrador'

    def test_reporte_proyecto(self):
        '''
        Test para generar el reporte de proyecto del sistema
        '''
        c = Client()
        c.login(username='juani', password='12345')

        resp = c.get('/reportes/proyecto/proyecto/2')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de proyecto sin permisos'
        c.login(username='admin', password='admin')
        resp = c.get('/reportes/proyecto/proyecto/2')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de proyecto con permisos'

    def test_reporte_lineasBase(self):
        '''
        Test para generar el reporte de proyecto del sistema
        '''
        c = Client()
        c.login(username='juani', password='12345')

        resp = c.get('/reportes/proyecto/lineasBase/2')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de lineas base sin permisos'
        c.login(username='admin', password='admin')
        resp = c.get('/reportes/proyecto/lineasBase/2')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de lineas base con permisos'

    def test_reporte_sc(self):
        '''
        Test para generar el reporte de sc de un proyecto
        '''
        c = Client()
        c.login(username='juani', password='12345')
        resp = c.get('/reportes/proyecto/solicitudesCambio/2')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de sc sin permisos'
        c.login(username='admin', password='admin')
        resp = c.get('/reportes/proyecto/solicitudesCambio/2')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de sc con permisos'

    def test_reporte_item(self):
        '''
        Test para generar el reporte de items de un proyecto
        '''
        c = Client()
        c.login(username='juani', password='12345')

        resp = c.get('/reportes/proyecto/items/2')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de items sin permisos'
        c.login(username='admin', password='admin')
        resp = c.get('/reportes/proyecto/items/2')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de items con permisos'

    def test_reporte_vitem(self):
        '''
        Test para generar el reporte de versiones de items de un proyecto
        '''
        c = Client()
        c.login(username='juani', password='12345')

        resp = c.get('/reportes/proyecto/versionesItems/2')
        self.assertEqual(resp.status_code, 302)
        print 'reporte de versiones de Items sin permisos'
        c.login(username='admin', password='admin')
        resp = c.get('/reportes/proyecto/versionesItems/2')
        self.assertEqual(resp.status_code, 200)
        print 'reporte de versiones de Items con permisos'