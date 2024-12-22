
from aplicaciones.ccjj.models import Acta, Expediente, Cliente, Especificacion, Informe, Parcial, Solicitante, Solicitud, Invitado
from aplicaciones.user.models import User

from datetime import date, datetime, timedelta

class ActaDoc():
        
    # Numero de Expediente
    def numExpediente(self, idexp):
        datofinal=''
        for i in Expediente.objects.filter(id = idexp):
            if int(i.num_exp) < 10:
                datofinal='00' + str(i.num_exp)
            elif int(i.num_exp) > 9:
                datofinal='0' + str(i.num_exp)

        return datofinal
    
    # Year Acta
    def yearActa(self, idexp):
        yearacta = ''
        for i in Informe.objects.filter(id_exp=idexp):
            return i.fec_inf.strftime("%Y")
            
    # Numero de Acta o Parcial
    def numActaParcial(self, idexp):
        datofinal = ''

        for i in Informe.objects.filter(id_exp=idexp):
            tipacta=i.tip_inf

        if tipacta == 'ci':
            for i in Parcial.objects.filter(id_inf__id_exp = idexp):
                if int(i.num_par) < 10:
                    datofinal='00' + str(i.num_par)
                elif int(i.num_par) > 9:
                    datofinal='0' + str(i.num_par)
        else:
            for i in Acta.objects.filter(id_inf__id_exp = idexp):
                if int(i.num_act) < 10:
                    datofinal='00' + str(i.num_act)
                elif int(i.num_act) > 9:
                    datofinal='0' + str(i.num_act)

        return datofinal

    # Tipo Informe Conciliacion (Acta o Parcial)
    def tipoInforme(self, idexp):
        datofinal=''
        tipacta=''

        for i in Informe.objects.filter(id_exp=idexp):
            tipacta=i.tip_inf
        
        if tipacta == 'at':
            datofinal = 'ACUERDO TOTAL'
        elif tipacta == 'ap':
            datofinal = 'ACUERDO PARCIAL'
        elif tipacta == 'fa':
            datofinal = 'FALTA DE ACUERDO'
        elif tipacta == 'is':
            datofinal = 'INASISTENCIA SOLICITANTE'
        elif tipacta == 'ii':
            datofinal = 'INASISTENCIA INVITADO'
        elif tipacta == 'iap':
            datofinal = 'INASISTENCIA DE AMBAS PARTES'
        elif tipacta == 'am':
            datofinal = 'ACTA MOTIVADA'
        elif tipacta == 'ci':
            datofinal = 'CONCLUSION CON INFORME'
        
        return datofinal
    
    # Hora Acta
    def hora(self):
        horaactual=datetime.now()
        return horaactual.strftime('%H:%M')
    
    # Fecha Acta
    def fechaActa(self, idexp):
        for i in Informe.objects.filter(id_exp = idexp):
            return i.fec_inf.strftime("%A %d de %B del año %Y")

    # Conciliador Acta
    def conciliadorActa(self, idexp):
        conciliador = ''   
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            conciliador = i.id_user.first_name + ' ' + i.id_user.last_name
        return conciliador
    
    # Conciliador DNI
    def conciliadorDNI(self, idexp):
        dni = ''   
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            if i.id_user.gen_user == 'm':
                dni = 'identificado con DNI N° ' + i.id_user.dni_user
            elif i.id_user.gen_user == 'f':
                dni = 'identificada con DNI N° ' + i.id_user.dni_user
        return dni
    
    # termino Conciliador
    def terminoConciliador(self, idexp):
        terminoconciliador=''
        
        for i in Expediente.objects.select_related('id_user').filter(id= idexp):
            if i.id_user.gen_user == 'm':
                terminoconciliador = 'Conciliador'
            elif i.id_user.gen_user == 'f':
                terminoconciliador = 'Conciliadora'
            else:
                terminoconciliador = 'Error'

        return terminoconciliador

    # Registro Conciliacion
    def registro(self, idexp):
        registro=''
        for i in Expediente.objects.select_related('id_esp').filter(id= idexp):
            if i.id_esp.id_pro.id_mat.id == 1:
                for i in Expediente.objects.select_related('id_user').filter(id= idexp):
                    if i.id_user.gen_user == 'm':
                        registro=i.id_user.rgg_user + ' y Registro Especializado en Familia N° ' + i.id_user.rgf_user + '.'
                    else:
                        registro=i.id_user.rgg_user + ' y Registro Especializada en Familia N° ' + i.id_user.rgf_user + '.'
            else:
                for i in Expediente.objects.select_related('id_user').filter(id= idexp):
                    registro = i.id_user.rgg_user
    
        return registro

    # Termino Solicitantes
    def terminoSolicitantes(self, idexp):
        termino=''
        cant=0
        for i in Solicitante.objects.filter(id_exp = idexp):
            cant=cant + 1
        if cant > 1:
            termino='las partes solicitantes'
        else:
            termino='la parte solicitante'
        return termino

    # Datos de Solicitantes
    def datosSolicitantes(self, idexp):
        terminodatossolicitantes = ''
        for i in Solicitante.objects.select_related('id_per').filter(id_exp=idexp):
            terminodatossolicitantes = terminodatossolicitantes + (i.id_per.nom_per 
            + ' ' + i.id_per.apepat_per
            + ' ' + i.id_per.apemat_per 
            + ' identificado con DNI N° ' + str(i.id_per.numdoc_per)
            + ', señala como domicilio en ' + i.id_per.dir_per
            + ', ')
        
        return terminodatossolicitantes
    
    # Termino Invitados
    def terminoInvitados(self, idexp):
        termino=''
        cant=0    
        for i in Invitado.objects.filter(id_exp = idexp):
            cant=cant + 1
        if cant > 1:
            termino='las partes invitadas'
        else:
            termino='la parte invitada'
        return termino

    # Datos Invitados
    def datosInvitados(self, idexp):
        terminodatosinvitados=''
        cant=Invitado.objects.filter(id_exp = idexp).count()

        for i in Invitado.objects.select_related('id_per').filter(id_exp=idexp):
                terminodatosinvitados = terminodatosinvitados + (i.id_per.nom_per 
                + ' ' + i.id_per.apepat_per
                + ' ' + i.id_per.apemat_per 
                + ' identificado con DNI N° ' + str(i.id_per.numdoc_per)
                + ', señala como domicilio en ' + i.id_per.dir_per
                + ', ')
        

        return terminodatosinvitados

    # Dato de Hechos
    def datosHechos(self, idexp):
        
        for i in Solicitud.objects.filter(id_exp=idexp):
            return i.hecdoc_sol

    # Dato de Descripcion
    def datosDescripcion(self, idexp):
        
        for i in Solicitud.objects.filter(id_exp=idexp):
            return i.pretactdoc_sol
    
    # Dato para Firmas
    def datosFirmas(self, idexp):
        
        datafirma=[]
        firmasolicitantes = ''
        firmainvitados = ''
        for s in Solicitante.objects.select_related('id_per').filter(id_exp = idexp):
            
            firmasolicitantes = firmasolicitantes + '\n\n\n ______________________ \n' + str(s.id_per.nom_per + ' ' + s.id_per.apepat_per + ' ' + s.id_per.apemat_per) + '\n' + str(s.id_per.numdoc_per) + '\n\n'
        
        for s in Invitado.objects.select_related('id_per').filter(id_exp = idexp):
            
            firmainvitados = firmainvitados + '\n\n\n ______________________ \n' + str(s.id_per.nom_per + ' ' + s.id_per.apepat_per + ' ' + s.id_per.apemat_per) + '\n' + str(s.id_per.numdoc_per) + '\n\n'
        
        resultado = firmasolicitantes + firmainvitados

        return resultado

     