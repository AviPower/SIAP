from django.db import models
from django.contrib.auth.models import User

'''
Clase que representa a un usuario en el sistema
'''

class Perfiles(models.Model):
    """
    Extender el modelo User para que incluyera otros campos y funciones
    No olvidar que los atributos de User son id, password, last_login, is_superuser, username,
    first_name, last_name, email, is_staff, is_active
    """
    usuario = models.OneToOneField(User)
    telefono = models.IntegerField(default=0,blank=True)
    '''
       telefono es numero telefonico perteneciente al usuario
    '''
    direccion = models.CharField(max_length=64,default='tu direccion',blank=True)
    '''
       direccion es direccion en la cual reside el usuario
    '''
    lider = models.BooleanField(null=False)
    '''
       representa si el usuario en cuestion es lider o no
    '''
    #foto = models.ImageField(upload_to='foto_usuario')
    '''
       Cargar foto del usuario y lo aloja en la carpeta foto_usuario
       necesidad de instalacion del PIL(Python Imaging LIbrary):
       http://www.mlewislogic.com/2011/09/how-to-install-python-imaging-in-a-virtualenv-with-no-site-packages/
    '''
    # no olvidar agregar mas adelante las relaciones solicitante(Solicitud) y votos(usuario)

    def __unicode__(self):
        return self.usuario.username
