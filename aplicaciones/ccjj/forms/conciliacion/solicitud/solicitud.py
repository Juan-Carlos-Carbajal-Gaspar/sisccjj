from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Solicitud
from datetime import datetime

class SolicitudForm(ModelForm):
    """Form definition for Solicitud."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['t'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for SolicitudForm."""

        model = Solicitud
        fields = '__all__'
        labels={

        }

        widgets={
            # 'fec_exp': forms.DateInput(
            #     format='%d-%m-%Y %H:%M:%S',
            #     attrs={
            #         'value': datetime.now().strftime('%d-%m-%Y %H:%M:%S'),
            #         'autocomplete': 'off',
            #         'readonly':'readonly',
            #     }
            # ),

        }
        # exclude=['num_exp','hor_exp','proini_exp','esttra_exp','estact_exp','audact_exp','numfol_exp','confin_exp','carp_exp','subcarpdf_exp','inv_exp','id_conf','id_esp','id_user']

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

