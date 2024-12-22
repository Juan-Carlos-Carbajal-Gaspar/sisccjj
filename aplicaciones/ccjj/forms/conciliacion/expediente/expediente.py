from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Expediente,Periodo
from datetime import datetime

class ExpedienteForm(ModelForm):
    """Form definition for Expediente."""
    
    
    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        fecha=datetime.now()
        
        self.fields['fec_exp'].initial = fecha.strftime('%d-%m-' + self.fechaHora() + ' %H:%M:%S')
        
    class Meta:
        """Meta definition for ExpedienteForm."""

        model = Expediente
        fields = '__all__'
        labels={

        }

        widgets={
            'fec_exp': forms.DateInput(
                
                # horaactual.strftime('%H:%M:%S')
                format='%d-%m-%Y %H:%M:%S',
                attrs={
                    'autocomplete': 'off',
                    'readonly':'readonly',
                }
            ),

        }
        exclude=['num_exp','hor_exp','proini_exp','esttra_exp','estact_exp','audact_exp','numfol_exp','confin_exp','inv_exp','id_pe','id_esp','id_user','estpro_exp']

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
    
    def fechaHora(self):
        for i in Periodo.objects.filter(est_pe='a'):
            return i.per_pe

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

