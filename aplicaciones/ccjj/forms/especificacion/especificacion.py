from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Especificacion
from datetime import datetime

class EspecificacionForm(ModelForm):
    """Form definition for Especificacion."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['des_esp'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for EspecificacionForm."""

        model = Especificacion
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

