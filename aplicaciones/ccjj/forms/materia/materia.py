from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Materia
from datetime import datetime

class MateriaForm(ModelForm):
    """Form definition for Materia."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['des_mat'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for MateriaForm."""

        model = Materia
        fields = '__all__'
        labels={

        }

        exclude=[]

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                form.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

