import json
import os
import io
from re import S

# IMPORTANDO MODELOS
from aplicaciones.ccjj.models import IngresoConciliacionDetalle, Persona, Periodo, IngresoCopias
from datetime import datetime, timedelta
from aplicaciones.user.models import User

class ReciboDatos:
    #Ingreso conciliacion
    def datosCliente(self, iddet):
        datres=''
        for i in IngresoConciliacionDetalle.objects.select_related().filter(id = iddet):
            for p in Persona.objects.filter(id = i.id_cli_id):
                datres = p.nom_per + ' ' + p.apepat_per + ' ' + p.apemat_per

        return datres
    
    def datosDNI(self, iddet):
        datres=''
        for i in IngresoConciliacionDetalle.objects.select_related().filter(id = iddet):
            for p in Persona.objects.filter(id = i.id_cli_id):
                datres = p.numdoc_per

        return datres

    def montoAbono(self, iddet):
        datres=''
        for i in IngresoConciliacionDetalle.objects.select_related().filter(id = iddet):
            datres = 'S/. ' + str(i.monadedet_con)
        return datres
    
    def yearExpediente(self):
        datres = ''
        for i in Periodo.objects.filter(est_pe='a'):
            datres=i.per_pe
        return datres

    # Ingreso copias
    def datosClienteCopias(self, idcop):
        datres=''
        for i in IngresoCopias.objects.select_related().filter(id = idcop):
            for p in Persona.objects.filter(id = i.id_cli_id):
                datres = p.nom_per + ' ' + p.apepat_per + ' ' + p.apemat_per

        return datres
    
    def datosDNICopias(self, idcop):
        datres=''
        for i in IngresoCopias.objects.select_related().filter(id = idcop):
            for p in Persona.objects.filter(id = i.id_cli_id):
                datres = p.numdoc_per

        return datres

    def montoAbonoCopias(self, idcop):
        datres=''
        for i in IngresoCopias.objects.select_related().filter(id = idcop):
            datres = 'S/. ' + str(i.monpag_cop)
        return datres