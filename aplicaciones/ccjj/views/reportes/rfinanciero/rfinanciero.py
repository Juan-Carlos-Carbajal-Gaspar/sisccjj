import json
import os

from datetime import datetime, timedelta

from django.shortcuts import render

# Importando modelos de Base de Datos
from aplicaciones.ccjj.models import Periodo, Expediente, Cliente, EgresoDetalle, IngresoCopias, CajaConciliacion, IngresoConciliacionDetalle
from django.db.models import Q, Avg, Count, Min, Sum

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Avg, Sum, Max, Min, Count
from django.db import transaction
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Importando la clase TemplateView
from django.views.generic.base import TemplateView

import locale
locale.setlocale(locale.LC_ALL, 'es_Pe')

# Permisos
from django.contrib.auth.mixins import LoginRequiredMixin
from aplicaciones.ccjj.mixins import ValidatePermissionRequiredMixin
# Creando nuestra vista para la Solicitud

class ReporteFinancieroView(LoginRequiredMixin, ValidatePermissionRequiredMixin, TemplateView):
    
    template_name = "reportes/rfinanciero/rfinanciero.html"
    permission_required = 'view_cajaconciliacion'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            
            # Para buscar los periodos registrados
            if action == 'searchperiodo':
                data = [{'id': 'all', 'text': 'Seleccione'}]
                for dy in Periodo.objects.all():                
                    data.append({'id': dy.per_pe, 'text': dy.per_pe }) 
                    
            elif action == 'datapago':
                
                periodo = request.POST['year']
                
                ingresos=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                egresos=[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
                
                # Ingresos
                nmesi=0
                for i in range(0,12):
                    nmesi = nmesi + 1

                    # Ingresos Conciliacion
                    datapagoingresos = IngresoConciliacionDetalle.objects.filter(fecingdet_con__year=periodo, fecingdet_con__month=nmesi)
                    totalsumaadelanto = sum(datapagoingresos.values_list('monadedet_con', flat=True))

                    # Ingresos Copias
                    datacopiaingresos = IngresoCopias.objects.filter(fec_cop__year=periodo, fec_cop__month=nmesi)
                    totalsumacopias = sum(datacopiaingresos.values_list('monpag_cop', flat=True))
                    if nmesi == i + 1:
                        ingresos[i]=float(totalsumaadelanto) + float(totalsumacopias)
                    else:
                        ingresos[i]=0.0
                            
                # Egresos
                nmese=0
                for i in range(0,12):
                    nmese = nmese + 1
                    datapagoegresos = EgresoDetalle.objects.filter(fecegredet_con__year=periodo, fecegredet_con__month=nmese)
                    totalsumaegreso = sum(datapagoegresos.values_list('monegre_det', flat=True))
                    if nmese == i + 1:
                        egresos[i]=float(totalsumaegreso)
                    else:
                        egresos[i]=0.0

                data={
                    'ingresos': ingresos,
                    'egresos': egresos
                }                   
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte Financiero'
        # context['forminicio']=ConfiguracionForm()
        context['titleform']='REPORTE FINANCIERO'
        context['numexp'] = self.kwargs.get('pk')
        context['action'] = 'addpagexp'
        
        return context
    

    
