
from aplicaciones.ccjj.models import Cliente, Expediente, Informe, IngresoConciliacion, Invitado, Parcial, Procedimiento, Acta, Solicitante, Solicitud

from datetime import datetime, timedelta

class ReportePorCliente():
    
     # Numero Expediente
    def numExpediente(self, idexp):
        dataresp = ''
        for i in Expediente.objects.filter(id = idexp):
            fechaexp = datetime.strptime(str(i.fec_exp), "%Y-%m-%d")
            dataresp = i.num_exp + '-' + str(fechaexp.year)         
        return dataresp
    
    # Solicitantes
    def datoSolicitantes(self, idexp):
    
        datasolicitante=''
        for i in Solicitante.objects.select_related('id_per').filter(id_exp=idexp):
            datasolicitante = datasolicitante + '*' + i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per 
                    
        return datasolicitante

    # Invitados
    def datoInvitados(self, idexp):
    
        datainvitado=''
        for i in Invitado.objects.select_related('id_per').filter(id_exp=idexp):
            datainvitado = datainvitado + '*' + i.id_per.nom_per + ' ' + i.id_per.apepat_per + ' ' + i.id_per.apemat_per
             
        return datainvitado

    # Fecha Solicitud
    def datoFechaSolicitud(self, idexp):
        datoresp=''
        for i in Solicitud.objects.filter(id_exp=idexp):
            datoresp = i.fecdoc_sol.strftime("%Y-%m-%d")
        return datoresp

    # Materia
    def datoMateria(self, idexp):
        datoresp=''
        for i in Expediente.objects.select_related('id_esp__id_pro').filter(id=idexp):
            datoresp = i.id_esp.id_pro.id_mat.des_mat
        return datoresp

    # Procedimiento
    def datoProcedimiento(self, idexp):
        datoresp=''
        for i in Expediente.objects.select_related('id_esp').filter(id=idexp):
            datoresp = i.id_esp.id_pro.des_pro
        return datoresp

    # Numero de Acta 
    def datoNumActa(self, idexp):
        datoresp=''
        for i in Acta.objects.filter(id_inf__id_exp=idexp):
            datoresp = i.num_act
        return datoresp

    # Numero de Informe
    def datoNumInforme(self, idexp):
        datoresp=''
        for i in Parcial.objects.filter(id_inf__id_exp=idexp):
            datoresp = i.num_par
        return datoresp

    # Tipo de Informe
    def datoTipoActa(self, idexp):
        datoresp=''
        for i in Informe.objects.filter(id_exp=idexp):
            datoresp = i.tip_inf
        return datoresp
    
    # Condicion Economica
    def datoCondicionEconomica(self, idexp):
        datoresp=''
        for i in IngresoConciliacion.objects.filter(idcaj_con__id_exp = idexp):
            datoresp = i.estado_con

        return datoresp
