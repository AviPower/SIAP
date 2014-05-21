__author__ = 'alvarenga'
from django import forms
from django.contrib.auth.models import Group, Permission


class GroupForm(forms.ModelForm):
    #permissions = Group.objects.exclude(permission_id=1,permission_id=2,permission_id=3)
    class Meta:
        model = Group
        #fields=['name','permissions']
