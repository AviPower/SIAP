from django.db import models

'''
Clase que representa a un usuario en el sistema
'''
class Usuario(models.Model):
    idUsuario = models.IntegerField(primary_key=True, null=False,unique=True)
    '''
       idUsuario representa la clave del usuario
    '''
    nombre = models.CharField(max_length=64, null=False)
    '''
       nombre es la denominacion que tiene el usuario, el nombre del mismo
    '''
    apellido = models.CharField(max_length=64, null=False)
    '''
       apellido es el apellido del usuario
    '''
    login = models.CharField(max_length=64, null=False,unique=True)
    '''
       login es la denominacion corta que tendra el usuario en lugar del nombre, en el momento de ingreso al sistema
    '''
    password = models.CharField(max_length=40, null=False)
    '''
       password es la contrasenha del usuario
    '''
    telefono = models.CharField(max_length=64, null=False)
    '''
       telefono es numero telefonico perteneciente al usuario
    '''
    direccion = models.CharField(max_length=64, null=False)
    '''
       direccion es direccion en la cual reside el usuario
    '''
    admin = models.BooleanField(null=False)
    '''
       representa si el usuario en cuestion es admin o no
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
        return self.login