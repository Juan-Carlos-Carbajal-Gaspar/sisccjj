from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Periodo
from datetime import datetime

class PeriodoForm(ModelForm):
    """Form definition for Periodo."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['per_pe'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for PeriodoForm."""

        model = Periodo
        fields = '__all__'
        labels={

        }

        # widgets={
        #     'id_per': forms.TextInput(
        #         attrs={
        #             'placeholder': ' Ingrese una Materia Conciliable',
        #             'required':'',
        #         }
        #     ),

        # }
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

