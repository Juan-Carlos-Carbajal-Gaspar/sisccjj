from django.forms import *
from aplicaciones.ccjj.models import *

class MateriaConciliacionForm(Form):
    materias = ModelChoiceField(queryset=Materia.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    procedimientos = ModelChoiceField(queryset=Procedimiento.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    especificaciones = ModelChoiceField(queryset=Especificacion.objects.none(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    