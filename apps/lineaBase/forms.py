__author__ = 'alvarenga'
from django import forms

from apps.lineaBase.models import LineaBase
from apps.items.models import Item


ESTADOS = (

    ('PEN', 'Pendiente'),
    ('VAL', 'Validado'),
)

class LineaBaseForm(forms.ModelForm):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.none(), widget=forms.CheckboxSelectMultiple(), required=True)
    def __init__(self, fase, *args, **kwargs):
        super(LineaBaseForm, self).__init__(*args, **kwargs)
        self.fields['items'].queryset = Item.objects.filter(estado='VAL', tipo_item__fase=fase.id, lineaBase=None)

    class Meta:
            model= LineaBase
            fields=['nombre',]

