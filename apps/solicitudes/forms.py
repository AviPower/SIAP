__author__ = 'marcel'


from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from apps.solicitudes.models import Voto, Solicitud
from django.contrib.admin.widgets import FilteredSelectMultiple



ESTADOS = (

    ('PEN', 'Pendiente'),
    ('APR','Aprobada'),
    ('REC', 'Rechazada'),
    ('REA','Ejecutada')
)


class SolicitudForm(ModelForm):

   # lider = forms.ModelChoiceField(queryset=User.objects.filter(is_active=True))
    #comite = forms.ModelMultipleChoiceField(queryset=User.objects.filter(is_active=True),
                                        #    widget=FilteredSelectMultiple("Comite", is_stacked=False))

    class Meta:
        model = Solicitud
        exclude = ['estado','roles']



class CambiarEstadoForm(ModelForm):
    estado = forms.CharField(max_length=3, widget=forms.Select(choices=ESTADOS))

    class Meta:
        model = Solicitud
        exclude = ['nombre', 'descripcion', 'fecha_ini', 'fecha_fin', 'lider', 'observaciones', 'comite']
