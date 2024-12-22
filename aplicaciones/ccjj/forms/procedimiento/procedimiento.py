from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Procedimiento
from datetime import datetime

class ProcedimientoForm(ModelForm):
    """Form definition for Procedimiento."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['des_pro'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for ProcedimientoForm."""

        model = Procedimiento
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

