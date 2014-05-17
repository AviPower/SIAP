from django import forms

from apps.items.models import Item


ESTADOS = (

    ('PEN', 'Pendiente'),
    ('FIN','Finalizado'),
    ('VAL', 'Validado'),
)

class PrimeraFaseForm(forms.ModelForm):
    class Meta:
        model= Item
        exclude=('estado', 'version', 'relacion', 'fecha_creacion', 'fecha_mod','tipo', 'tipo_item')

class EstadoItemForm(forms.ModelForm):
    estado=forms.CharField(max_length=3,widget=forms.Select(choices= ESTADOS))
    class Meta:
        model=Item
        fields=['estado']
