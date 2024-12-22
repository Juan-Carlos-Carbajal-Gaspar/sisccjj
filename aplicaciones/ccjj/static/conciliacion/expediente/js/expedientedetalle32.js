// Funcion Para completar automaticamente la fecha y hora
function completarFecha(){
    var fecha = new Date(); //Fecha actual
    var mes = fecha.getMonth()+1; //obteniendo mes
    var dia = fecha.getDate(); //obteniendo dia
    var ano = fecha.getFullYear(); //obteniendo año
    // var hora = fecha.getHours(); //obteniendo hora
    // var minutos = fecha.getMinutes(); //obteniendo minuto
    
    return ano+"-"+minTwoDigits(mes)+"-"+minTwoDigits(dia + 1);
    
}

// Funcion para establecer minimo dos digitos para la fecha y hora automaticamente
function minTwoDigits(n) {
    return (n < 10 ? '0' : '') + n;
}

var tblExpedienteDetalle;

function getData(){
      tblExpedienteDetalle=$('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        search: false,
        searching: false,
        paging: false,
        bInfo: false,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'listaexpedientedetalle'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "numexp"},
            {"data": "fecha"},
            {"data": "solicitud"},
            {"data": "numexp"},
            {"data": "numexp"},
            {"data": "exicaja"},
            {"data": "numexp"},
            {"data": "numexp"},
            {"data": "numexp"},
        ],
        columnDefs: [
            {
                targets: [-9], // Numero de Expediente Expediente
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var fecyear = new Date(row.fecha);
                    var year = fecyear.getFullYear();
                    return row.numexp + " - " + year;
                }
            },
            {
                targets: [-8], // Fecha y Hora Expediente
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.fecha + ' - ' + row.hora;
                }
            },
            {
                targets: [-7], // Solicitud
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estpro=='exp'){
                        return ' <a href="#" rel="expsolicitud" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Generar</a>';
                    }
                    return 'Solicitud Generada';
                    
                }
            },
            {
                targets: [-6], // Materia Conciliable
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estpro=='exp'){
                        return 'Genere la Solicitud';
                    }
                    else if (row.estpro=='sol'){
                        return ' <a href="#" rel="expmateria" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>';
                    }
                    else{
                        return 'Materia Seleccionada';
                    }                   
                }
            },
            {
                targets: [-5], // Esquela Conciliador
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estpro=='exp'){
                        return 'Genere la Solicitud';
                    }
                    else if (row.estpro=='sol'){
                        return 'Seleccione la Materia Conciliable';
                    }
                    else if (row.estpro=='mat'){
                        if (row.idusuario == '1'){
                            return ' <a href="#" rel="expconciliador" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>'; 
                        }
                        return 'Usted no tiene permiso';
                    }
                    else{
                        return 'Esquela Generada';
                    }
                    /////
                    // if (row.idusuario == '1'){
                    //     if (row.estpro=='exp'){
                    //         return 'Genere la Solicitud';
                    //     }
                    //     else if (row.estpro=='sol'){
                    //         return 'Seleccione la Materia Conciliable';
                    //     }
                    //     else if (row.estpro=='mat'){
                    //         return ' <a href="#" rel="expconciliador" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>'; 
                    //     }
                    //     else{
                    //         return 'Esquela Generada';
                    //     }
                    // }else{
                    //     if (row.estpro=='exp'){
                    //         return 'Genere la Solicitud';
                    //     }
                    //     else if (row.estpro=='sol'){
                    //         return 'Seleccione la Materia Conciliable';
                    //     }
                    //     else if (row.estpro=='mat'){
                           
                    //         return 'Conciliador'; 
                    //     }
                    //     else{
                    //         return 'Esquela Generada';
                    //     }   
                    // }   
                       
                }
            },
           
            {
                targets: [-4], // Invitacion Expediente
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(row.tipcon == 'ma'){
                        return 'Mismo Acto';
                    }
                    else if (row.tipcon == 'ci'){
                        if (row.estpro=='exp'){
                            return 'Genere la Solicitud';
                        }
                        else if (row.estpro=='sol'){
                            return 'Seleccione la Materia Conciliable';
                        }
                        else if (row.estpro=='mat'){
                            if (row.idusuario != 1){
                                return '<a href="#" rel="expinvitacion" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Generar</a>';
                            }
                            return 'Genere Esquela Conciliador';
                            
                        }
                        else if (row.estpro=='esq'){
                            return '<a href="#" rel="expinvitacion" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Generar</a>';
                        }
                        else if (row.estpro=='inv'){
                            return '<a href="#" rel="expinvitacion" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Generar</a>';
                        }
                        else if (row.estpro=='caj'){
                            return '<a href="#" rel="expinvitacion" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Generar</a>';
                        } 
                        else if (row.estpro=='act'){
                            return '<a href="#" rel="expinvitacion" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Generar</a>';
                        }                        
                    }
                    else{
                        return 'Error';
                    }
                    
                }
            },
            {
                targets: [-3], // Pago Expediente
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estpro=='exp'){
                        return 'Genere la Solicitud';
                    }
                    else if (row.estpro=='sol'){
                        return 'Seleccione la Materia Conciliable';
                    }
                    else if (row.estpro=='mat'){
                        if (row.idusuario != 1){
                            if (row.tipcon == 'ma'){
                                return ' <a href="#" rel="exppago" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>';
                            }else{
                                return 'Genere las Invitaciones';
                            }
                        }
                        return 'Genere Esquela Conciliador';
                        
                    }
                    else if (row.estpro=='esq'){
                        return 'Genere las Invitaciones';
                    }
                    else if (row.estpro=='inv'){
                        return ' <a href="#" rel="exppago" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>';                       
                    }
                    else if (row.estpro=='caj'){
                        return ' <a href="#" rel="exppago" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>';                       
                    }
                    else if (row.estpro=='act'){
                        return ' <a href="#" rel="exppago" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Registrar</a>';
                    }else{
                        return 'error';
                    }
                    
                }
            },
            {
                targets: [-2], // Acta Expediente
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estpro=='exp'){
                        return 'Genere la Solicitud';
                    }
                    else if (row.estpro=='sol'){
                        return 'Seleccione la Materia Conciliable';
                    }
                    else if (row.estpro=='mat'){
                        if (row.idusuario != 1){
                            if(row.tipcon == 'ma'){
                                return 'Registre Caja Expediente';
                            }
                            return 'Genere las Invitaciones';
                        }
                        return 'Genere Esquela Conciliador';
                    }
                    else if (row.estpro=='esq'){
                        return 'Genere las invitaciones';
                    }
                    else if (row.estpro=='inv'){
                        return 'Registre Caja Conciliacion'
                    }
                    else if (row.estpro=='caj'){
                        if(row.tipcon == 'ma'){
                            return ' <a href="#" rel="expacta" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Ir</a>';
                        }else{
                            if (row.fechaaudiencia == row.fechaactual){
                                return ' <a href="#" rel="expacta" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Ir</a>';
                            }else{
                                return 'Esperar la fecha de audiencia';
                            }
                        }                      
                        
                    }
                    else if (row.estpro=='act'){
                        return ' Acta generada';
                    }
                    else{
                        return 'Error';
                    }
                    
                }
            },
            {
                targets: [-1], // Documentos
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if (row.estpro!='exp'){
                        return ' <a href="#" rel="expdocumentos" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Ir</a>';
                    }
                    return 'Genere la Solicitud';
                    
                }
            },
                        
        ],
        initComplete: function (settings, json) {
            // alert("Tabla Cargada");
        }
      });
}

$(function () {
      
    // Para Cargar los datos a la tabla
    getData();    

    // -------------------------------//
    //---TABLA EXPEDIENTE DETALLE-------------//
    //--------------------------------//
    // Para Expediente Detalle
    $('#data tbody')
        // Ver Solicitud
        .on('click', 'a[rel="expsolicitud"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();

            window.location.href='/expediente/expedientesolicitud/'+ data.id + '/';
        })
        // Ver Materia de Conciliacion
        .on('click', 'a[rel="expmateria"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();

            window.location.href='/expediente/expedientemateriaconciliacion/'+ data.id + '/';
        })
        // Ver Esquela Conciliador
        .on('click', 'a[rel="expconciliador"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();

            window.location.href='/expediente/expedienteesquelaconciliador/'+ data.id + '/';
        })
        // Ver Invitacion Conciliador
        .on('click', 'a[rel="expinvitacion"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();
            
            window.location.href='/expediente/invitacion/'+ data.id + '/';
            
        })
        // Ver Pago Conciliacion
        .on('click', 'a[rel="exppago"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();
            if (data.exicaja == 1){
                window.location.href='/expediente/cajaconciliacion/'+ data.id + '/';
            }
            else{
                window.location.href='/expediente/expedientepago/'+ data.id + '/';
            }
            
        })
        // Ver Acta Conciliacion
        .on('click', 'a[rel="expacta"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();

                window.location.href='/genactaconciliacion/'+ data.id + '/';
                      
            
        })
        // Ver Documentos Conciliacion
        .on('click', 'a[rel="expdocumentos"]', function () {
            var tr = tblExpedienteDetalle.cell($(this).closest('td, li')).index();
            var data = tblExpedienteDetalle.row(tr.row).data();

            window.location.href='/listadocumentos/'+ data.id + '/';
            
        })
    // -------------------------------//
    //---TABLA EXPEDIENTE DETALLE-------------//
    //--------------------------------//

});
  
  