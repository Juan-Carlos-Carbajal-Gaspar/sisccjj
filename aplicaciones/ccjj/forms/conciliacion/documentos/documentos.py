from django.forms import *
from django import forms
from aplicaciones.ccjj.models import Documento
from datetime import datetime

class DocumentoForm(ModelForm):
    """Form definition for Documento."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['t'].widget.attrs['autofocus'] = True

    class Meta:
        """Meta definition for DocumentoForm."""

        model = Documento
        fields = '__all__'
        labels={

        }

        widgets={
            #'arcesc_doc': forms.FileField(
            #    attrs={
            #        'class':'form-control',
            #    }
            #),

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
