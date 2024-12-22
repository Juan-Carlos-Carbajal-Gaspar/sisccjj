from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Socio, Persona
from datetime import datetime

class SocioForm(ModelForm):
    """Form definition for Socio."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nom_per'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for SocioForm."""

        model = Persona
        fields = '__all__'
        labels={

        }

        """widgets={
            'cod_soc': forms.TextInput(
                attrs={
                    'placeholder': ' Ingrese un Socio',
                    'required':'',
                }
            ),

        }"""
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

    # def clean(self):
    #    cleaned = super().clean()
    #    if len(cleaned['name']) <= 50:
    #        raise forms.ValidationError('Validacion xxx')
    #        #self.add_error('name', 'Le faltan caracteres')
    #    return cleaned

    # def clean_nomb_cli(self):
    #     nombre = self.cleaned_data['nomb_cli']
    #     if not nombre.isalpha():
    #         raise forms.ValidationError('El nombre no puede contener números')
    #     return nombre

