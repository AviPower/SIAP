
from django.contrib.auth.models import User
from django.forms import ModelForm
from django import forms
from apps.solicitudes.models import Voto



class VotoForm(forms.ModelForm):
    class Meta:
        model=Voto
        fields=['voto']
