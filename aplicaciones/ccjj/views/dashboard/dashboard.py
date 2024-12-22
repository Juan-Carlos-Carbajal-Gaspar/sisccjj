from django.shortcuts import render, redirect, HttpResponseRedirect

from django.contrib.auth.decorators import login_required
from django.db import models
from django.db import transaction
from django.http.response import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from aplicaciones.ccjj.models import Agenda, Expediente, Cliente, Especificacion, Solicitud, Acta

import json
import os

from datetime import datetime
import locale
locale.setlocale(locale.LC_ALL, 'es_Pe')

# Importando la clase TemplateView
from django.views.generic.base import TemplateView

# Creando nuestra vista para el Dashboard

class DashboardView(TemplateView):

    template_name = "dashboard/dashboard.html"

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)
    
    def cantidadAudiencias(self):
        cantidad=Agenda.objects.count()
        return cantidad
    
    def cantidadHoy(self):
        classfechaactual=datetime.now()
        cant=0
        for i in Agenda.objects.all():
            if classfechaactual.strftime("%Y-%m-%d") == i.fecaud_age.strftime("%Y-%m-%d"):
                cant=cant + 1
        return cant
    
    def cantidadSemana(self):
        classfechaactual=datetime.now()
        cant=0
        for i in Agenda.objects.all():
            if classfechaactual.strftime("%W") == i.fecaud_age.strftime("%W"):
                cant=cant + 1
        return cant
    
    def cantidadOtros(self):
        classfechaactual=datetime.now()
        cant=0
        for i in Agenda.objects.all():
            if classfechaactual.strftime("%W") < i.fecaud_age.strftime("%W"):
                cant=cant + 1
        return cant
    
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'searcheventos':

                # Para actualizar los colores de la hoy, esta semana y otras semanas
                classfechaactual=datetime.now()
               
                for item in Agenda.objects.all():
                    # Para hoy
                    if classfechaactual.strftime("%Y-%m-%d") == item.fecaud_age.strftime("%Y-%m-%d"):
                        actage=Agenda.objects.get(pk=item.id)
                        actage.foncolor_age ='#0FB925'
                        actage.borcolor_age='#0FB925'
                        actage.save()
                    # Otras semanas
                    elif classfechaactual.strftime("%W") < item.fecaud_age.strftime("%W"):
                        actage=Agenda.objects.get(pk=item.id)
                        actage.foncolor_age='#cc0000'
                        actage.borcolor_age='#cc0000'
                        actage.save()
                    # Para esta semana
                    elif classfechaactual.strftime("%W") == item.fecaud_age.strftime("%W"):
                        actage=Agenda.objects.get(pk=item.id)
                        actage.foncolor_age='#FF9326'
                        actage.borcolor_age='#FF9326'
                        actage.save()

                # Para mostrar Eventos en Calendario
                dataevento = []
                eventos = {}

                dataconsulta = ''
                if (request.user.id == 1):
                    dataconsulta = Agenda.objects.all()
                else:
                    dataconsulta = Agenda.objects.filter(id_exp__id_user = request.user.id)

                for i in dataconsulta:
                    eventos['title'] = i.tit_age
                    eventos['start'] = i.fecaud_age.strftime("%Y-%m-%dT%H:%M")
                    eventos['allDay'] = 'false'
                    # eventos['url'] = "reverse_lazy('ccjj:jj_listacliente')"
                    # eventos['url'] = "ccjj:jj_listacliente"
                    eventos['url'] = '/expediente/expedientedetalle/' + str(i.id_exp_id) + '/'
                    eventos['backgroundColor'] = i.foncolor_age
                    eventos['borderColor'] = i.borcolor_age

                    dataevento.append(eventos)

                    eventos = {}
                    
                return JsonResponse(dataevento, safe=False)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Dashboard'
        context['titlecalendar'] = 'CRONOGRAMA DE AUDIENCIAS DE LOS EXPEDIENTES'
        context['cantaudiencias'] = self.cantidadAudiencias()
        context['canthoy'] = self.cantidadHoy()
        context['cantsemana'] = self.cantidadSemana()
        context['cantotros'] = self.cantidadOtros()
        return context