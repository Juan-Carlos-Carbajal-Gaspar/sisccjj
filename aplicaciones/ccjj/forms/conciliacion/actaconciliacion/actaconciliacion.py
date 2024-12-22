from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Informe, Persona, Cliente
from datetime import datetime

class ActaConciliacionForm(ModelForm):
    """Form definition for ActaConciliacionForm."""

    def __init__(self, fechahora, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fec_inf'].initial=fechahora

    class Meta:
        """Meta definition for ActaConciliacionForm."""

        model = Informe
        fields = '__all__'
        labels={

        }

        widgets={
            'fec_inf': forms.TextInput(
                attrs={
                    'readonly': 'readonly',
                    'class': 'form-control',
                }
            ),
            'tip_inf': forms.Select(
                attrs={
                    'class': 'form-control'
                }
            ),

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

