from django.forms import *
from django import forms
from aplicaciones.ccjj.models import IngresoConciliacion, Cliente, Socio
from datetime import datetime

class IngresoConciliacionForm(ModelForm):
    """Form definition for IngresoConciliacionForm."""
    
    def __init__(self, pagtotal_pag, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pacpag_con'].initial=pagtotal_pag
        self.fields['descuento'].widget.attrs['max']=(float(pagtotal_pag) - 1)
        self.fields['adelanto'].widget.attrs['max']=(float(pagtotal_pag))
        
    class Meta:
        """Meta definition for IngresoConciliacionForm."""

        model = IngresoConciliacion
        fields = '__all__'
        
        widgets={
            'pacpag_con': forms.NumberInput(
                attrs={
                    'readonly':'readonly',
                    'class': 'form-control'
                }
            ),
            
        }
        # exclude=['estatotal_pag','totalcaja_pag', 'totalpasaje_pag']

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
    
    socios = ModelChoiceField(queryset=Socio.objects.select_related('id_per').all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: auto'
    }))

    descuento = DecimalField(widget=NumberInput(attrs={
        'value':'0',
        'class': 'form-control',
        'min': '0'
    }))

    adelanto = DecimalField(widget=NumberInput(attrs={
        'value':'0',
        'class': 'form-control',
        'min': '0'
    }))

    montocopias = DecimalField(widget=NumberInput(attrs={
        'value':'0',
        'class': 'form-control',
        'min': '0'
    }))

    cantidadcopias = DecimalField(widget=NumberInput(attrs={
        'value':'0',
        'class': 'form-control',
        'min': '0'
    }))
    

    # Egresos
    montoegresos = DecimalField(widget=NumberInput(attrs={
        'value':'0',
        'class': 'form-control',
        'min': '0',
    }))

    # def clean(self):
    #    cleaned = super().clean()
    #    if len(cleaned['name']) <= 50:
    #        raise forms.ValidationError('Validacion xxx')
    #        #self.add_error('name', 'Le faltan caracteres')
    #    return cleaned