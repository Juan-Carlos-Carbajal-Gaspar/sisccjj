
from aplicaciones.ccjj.models import Acta, Expediente, Cliente, Especificacion, Invitacion, Persona, Solicitante, Solicitud
from aplicaciones.user.models import User

from datetime import datetime, timedelta

class InvitacionDoc():

    # Numero de Expediente
    def numExpediente(self, idexp):
        datofinal=''
        for i in Expediente.objects.filter(id = idexp):
            if int(i.num_exp) < 10:
                datofinal='00' + str(i.num_exp)
            elif int(i.num_exp) > 9:
                datofinal='0' + str(i.num_exp)

        return datofinal
    
    # Year Expediente   
    def yearExpediente(self, idexp):
        for i in Expediente.objects.filter(pk = idexp):
            fechainvitacion = datetime.strptime(str(i.fec_exp), "%Y-%m-%d")
            return fechainvitacion.year

    # Datos de Solicitantes
    def datosSolicitantes(self, idexp):
        terminodatossolicitantes = ''
        for i in Solicitante.objects.select_related('id_per').filter(id_exp = idexp):
            terminodatossolicitantes = terminodatossolicitantes + (i.id_per.nom_per 
            + ' ' + i.id_per.apepat_per
            + ' ' + i.id_per.apemat_per 
            + ', ')

        return terminodatossolicitantes

    # Direccion Solicitantes
    def datosDireccionSolicitantes(self, idexp):
        terminodatossolicitantes = ''
        for i in Solicitante.objects.select_related('id_per').filter(id_exp = idexp):
            terminodatossolicitantes = terminodatossolicitantes + (i.id_per.dir_per + ', ')
        return terminodatossolicitantes

    # Datos Invitados
    def datosInvitados(self, idper):
        terminodatosinvitados=''
        for i in Persona.objects.filter(id=idper):
            terminodatosinvitados = i.nom_per + ' ' + i.apepat_per + ' ' + i.apemat_per
        return terminodatosinvitados

    # Datos Direccion Invitados
    def datosDireccionInvitados(self, idper):
        terminodatosinvitados=''
        for i in Persona.objects.filter(id=idper):
            terminodatosinvitados = i.dir_per
        return terminodatosinvitados
    
    # Dato de Descripcion
    def datosPretensionSol(self, idexp):
        pretension=''
        for i in Solicitud.objects.filter(id_exp = idexp):
            pretension = i.pretsoldoc_sol
        return pretension

     