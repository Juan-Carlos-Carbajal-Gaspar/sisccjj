import json
import os
import io
from re import S

# IMPORTANDO MODELOS
from aplicaciones.ccjj.models import Conciliador, Expediente, Periodo, Invitado, Solicitante, Solicitud
from datetime import datetime, timedelta
from aplicaciones.user.models import User


class EsquelaConciliadorDatos:

    def fecha(self):
        fechaactual=datetime.now()
        for i in Periodo.objects.filter(est_pe='a'):
            fechaexp=i.per_pe
        return fechaexp + '-' + fechaactual.strftime("%m-%d")
    
    def hora(self):
        horaactual=datetime.now()
        return horaactual.strftime('%H:%M:%S')
    
    # Datos para plantilla Documento Esquela Conciliador
    # Numero de Expediente    
    def numExpediente(self, idexp):
        datofinal=''
        for i in Expediente.objects.filter(pk=idexp):
            if int(i.num_exp) < 10:
                datofinal='00' + str(i.num_exp)
            elif int(i.num_exp) > 9:
                datofinal='0' + str(i.num_exp)
        
        return datofinal
    
    # Year Expediente   
    def yearExpediente(self, idexp):
        for i in Conciliador.objects.filter(id_exp=idexp):
            fechaesqcon = datetime.strptime(str(i.fec_doc), "%Y-%m-%d")
            return fechaesqcon.year

    # termino Conciliador
    def terminoConciliador(self, idexp):
        terminoconciliador=''
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            if i.id_user.gen_user == 'm':
                terminoconciliador='Señor Conciliador'
            elif i.id_user.gen_user == 'f':
                terminoconciliador='Señora Conciliadora'

        return terminoconciliador

    # Datos de Conciliador
    def datosConciliador(self, idexp):
        conciliador = ''
        
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            conciliador=i.id_user.first_name + ' ' + i.id_user.last_name
        return conciliador
    
    # Dato de Registro No Familia
    def datosRegistroNoFamilia(self, idexp):
        registro=''
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            registro=i.id_user.rgg_user

        return registro

    # # Dato de datosRegistroFamilia
    def datosRegistroFamilia(self, idexp):
        registrofamilia=''
        idmat=0
        for i in Expediente.objects.select_related('id_esp').filter(id= idexp):
            idmat = i.id_esp.id_pro.id_mat.id
        
        if idmat == 1:
            for i in Expediente.objects.select_related('id_user').filter(id= idexp):
                if i.id_user.gen_user == 'm':
                    registrofamilia=' y Registro Especializado en Familia N° ' + i.id_user.rgf_user + '.'
                else:
                    registrofamilia=' y Registro Especializada en Familia N° ' + i.id_user.rgf_user + '.'
        else:
            registrofamilia='.'         
            
            
        return registrofamilia

    # Dato de datosTermDesignacion
    def datosTermDesignacion(self, idexp):
        terminodesignacion=''
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            if i.id_user.gen_user == 'm':
                terminodesignacion='designado como Conciliador'
            else:
                terminodesignacion='designada como Conciliadora'

        return terminodesignacion
    
    # Dato Solicitantes
    def datosSolicitantes(self, idexp):
        datossolicitantes = ''
        for i in Solicitante.objects.select_related('id_per').filter(id_exp=idexp):
            datossolicitantes = datossolicitantes + (i.id_per.nom_per
            + ' ' + i.id_per.apepat_per
            + ' ' + i.id_per.apemat_per            
            + ', ')
        
        return datossolicitantes.upper()
    
    # Dato Invitados
    def datosInvitados(self, idexp):
        datosinvitados = ''
        for di in Expediente.objects.filter(id=idexp):
            if di.tipcon_exp == 'ma':
                return '.'
            else:
                for i in Invitado.objects.select_related('id_per').filter(id_exp=idexp):
                    datosinvitados = datosinvitados + (i.id_per.nom_per
                    + ' ' + i.id_per.apepat_per
                    + ' ' + i.id_per.apemat_per            
                    + ', ')
                return ' invitando a ' + datosinvitados.upper()

    # Dato datosProcedimiento
    def datosProcedimiento(self, idexp):
        procedimiento=''

        for i in Expediente.objects.select_related('id_esp').filter(id=idexp):
            procedimiento=i.id_esp.id_pro.des_pro

        return procedimiento
