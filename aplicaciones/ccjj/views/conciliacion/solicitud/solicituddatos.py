# IMPORTANDO MODELOS
from aplicaciones.ccjj.models import Expediente, Periodo, Invitado, Solicitante, Solicitud
from datetime import datetime

class SolicitudDatos:
    def year(self):
        for i in Periodo.objects.filter(est_pe='a'):
            return i.per_pe
        
    def fecha(self):
        fechaactual=datetime.now()
        for i in Periodo.objects.filter(est_pe='a'):
            fechaexp=i.per_pe
        return fechaexp + '-' + fechaactual.strftime("%m-%d")
    
    def tipoConciliacion(self, idexp):
        for i in Expediente.objects.filter(pk=idexp):
            return i.tipcon_exp
        
    def numSolicitud(self, idexp):
        datofinal=''
        for i in Expediente.objects.filter(pk=idexp):
            if int(i.num_exp) < 10:
                datofinal='00' + str(i.num_exp)
            elif int(i.num_exp) > 9:
                datofinal='0' + str(i.num_exp)
        
        return datofinal

    # Datos para plantilla Documento Solicitud 
    # Year Solicitud
    def yearSolicitud(self, idexp):
        for i in Solicitud.objects.filter(id_exp=idexp):
            fechasol = datetime.strptime(str(i.fecdoc_sol), "%Y-%m-%d")
            return fechasol.year

    # Termino Solicitante para solicitud
    def terminoSolicitante(self, idexp):
        terminosolicitante=''
        cant=0
        datossolicitante=Solicitante.objects.filter(id_exp = idexp)
        for i in datossolicitante:
            cant=cant + 1

        if cant > 1:
            terminosolicitante='SOLICITANTES'
        else:
            terminosolicitante='SOLICITANTE'

        return terminosolicitante

    # Datos de Solicitantes para Solicitud
    def datosSolicitantes(self, idexp):
        terminodatossolicitantes = ''
        # datossolicitantesexp = ClienteExpediente.objects.select_related('sol_soli').filter(exp_id=numexpsol, tipcli_exp='s')
        cantsoli=Solicitante.objects.filter(id_exp = idexp).count()

        if cantsoli == 1:
            datossolicitantesexp = Solicitante.objects.select_related('id_per').filter(id_exp=idexp)
            for i in datossolicitantesexp:
                terminodatossolicitantes = i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per + ' identificado con DNI N° ' + str(i.id_per.numdoc_per) + ' señala como domicilio en ' + i.id_per.dir_per + '.'
        elif cantsoli > 1:
            datossolicitantesexp = Solicitante.objects.select_related('id_per').filter(id_exp=idexp)
            for i in datossolicitantesexp:
                terminodatossolicitantes = terminodatossolicitantes + (i.id_per.nom_per 
                + ' ' + i.id_per.apepat_per
                + ' ' + i.id_per.apemat_per 
                + ' identificado con DNI N° ' + str(i.id_per.numdoc_per)
                + ' señala como domicilio en ' + i.id_per.dir_per
                + ', ')

        return terminodatossolicitantes
    
    # Dato de Terminio de Inicio para Solicitud
    def datosTerminoInicio(self, idexp):
        terminoinicio=''
        cant=0
        datossolicitante=Solicitante.objects.filter(id_exp = idexp)
        for i in datossolicitante:
            cant=cant + 1

        if cant > 1:
            terminoinicio='Nos dirigimos'
        else:
            terminoinicio='Me dirijo'

        return terminoinicio

    # Dato de Hechos para la Solicitud
    def datoHechos(self, idexp):
        terminohechos=''

        datoshechossol=Solicitud.objects.filter(id_exp=idexp)
        for i in datoshechossol:
            terminohechos = i.hecdoc_sol
        return terminohechos

    # Dato de Pretension para la Solicitud
    def datoPretension(self, idexp):
        terminopretension=''

        datospretensionsol=Solicitud.objects.filter(id_exp=idexp)
        for i in datospretensionsol:
            terminopretension = i.pretsoldoc_sol
        return terminopretension
    
    # Dato para termino de invitacion para la Solicitud
    def terminoInvitacion(self, idexp):
        terminoinvitacion=''

        datotipcon=Expediente.objects.filter(id=idexp)
        for i in datotipcon:
            if i.tipcon_exp == 'ma':
                terminoinvitacion = ''
            elif i.tipcon_exp == 'ci':
                terminoinvitacion = 'Para lo cual se debe invitar al (los) Señor (es):'
            else:
                terminoinvitacion = ''

        return terminoinvitacion

    # Dato para termino de invitados para la solicitud
    def terminoInvitado(self, idexp):
        terminoinvitado=''
        cant=0
        datosinvitado=Invitado.objects.filter(id_exp = idexp)
        for i in datosinvitado:
            cant=cant + 1

        if cant > 1:
            terminoinvitado='Invitados (as):'
        elif cant == 1:
            terminoinvitado='Invitado (a):'

        return terminoinvitado

    # Datos de Invitados
    def datosInvitados(self, idexp):
        terminodatosinvitados=''

        cantinv=Invitado.objects.filter(id_exp = idexp).count()

        if cantinv == 1:
            datosinvitadosexp = Invitado.objects.select_related('id_per').filter(id_exp=idexp)
            for i in datosinvitadosexp:
                terminodatosinvitados = i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per + ' identificado con DNI N° ' + str(i.id_per.numdoc_per) + ' señala como domicilio en ' + i.id_per.dir_per + '.'
        elif cantinv > 1:
            datosinvitadosexp = Invitado.objects.select_related('id_per').filter(id_exp=idexp)
            for i in datosinvitadosexp:
                terminodatosinvitados = terminodatosinvitados + (i.id_per.nom_per 
                + ' ' + i.id_per.apepat_per
                + ' ' + i.id_per.apemat_per 
                + ' identificado con DNI N° ' + str(i.id_per.numdoc_per)
                + ' señala como domicilio en ' + i.id_per.dir_per
                + ', ')

        return terminodatosinvitados

    # Dato para termino de DNI
    def terminoDni(self, idexp):
        terminodni=''

        cant=0
        datossolicitante=Solicitante.objects.filter(id_exp = idexp)
        for i in datossolicitante:
            cant=cant + 1

        if cant > 1:
            terminodni='de los Solicitantes'
        else:
            terminodni='del Solicitante'

        return terminodni

    
        