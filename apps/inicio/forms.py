__author__ = 'alvarenga'
from django import forms
from django.contrib.auth.forms import UserCreationForm

class UserForm(UserCreationForm):
    first_name = forms.CharField(label=("Nombre"))
    last_name = forms.CharField(label=("Apellido"))
    email = forms.EmailField(label=("correo electronico"))
    telefono = forms.IntegerField()
    direccion = forms.CharField(max_length=64)