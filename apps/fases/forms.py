__author__ = 'marcel'

from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from apps.fases.models import Fase
from django.contrib.admin.widgets import AdminDateWidget, FilteredSelectMultiple
from django.core.exceptions import ValidationError


ESTADOS = (
    ('PEN', 'Pendiente'),
    ('DES', 'Desarrollo'),
    ('COMPL', 'Completa'),
    ('COMPR', 'Comprometida'),
)


class FaseForm(forms.ModelForm):
    nombre = forms.CharField(max_length=100)
    descripcion = forms.CharField(label='Descripcion', widget=forms.Textarea)
    posicion = forms.DecimalField(label='Posicion de la Fase dentro del Proyecto')
    maxItems = forms.DecimalField(label='Cantidad de Items')
    orden = forms.DecimalField(label='Orden de Items')
    fecha_ini = forms.DateField(widget=AdminDateWidget, label='Fecha de Inicio')
    fecha_fin = forms.DateField(widget=AdminDateWidget, label='Fecha de finalizacion')

    class Meta:
        model = Fase
        exclude = ['estado']


class CambiarEstadoForm(forms.ModelForm):
    estado = forms.CharField(max_length=4, widget=forms.Select(choices=ESTADOS))

    class Meta:
        model = Fase
        exclude = ['nombre', 'descripcion', 'posicion', 'maxItems', 'orden', 'fecha_ini', 'fecha_fin', 'lider']
