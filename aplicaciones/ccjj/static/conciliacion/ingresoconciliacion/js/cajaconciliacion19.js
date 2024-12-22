var tblIngresoDetalleConciliacion;
var tblIngresoCopiasCertificadas;
var tblEgresosConciliacion;
var tblCajaConciliacion;
function getData(){
    // TABLA INGRESO CONCILIACION
    tblIngresoDetalleConciliacion=$('#tblIngresoDetalle').DataTable({
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
                'action': 'listaingresodetalleconciliacion'
            },
            dataSrc: ""
        },
        columns: [  
            {"data": "fechapago"},
            {"data": "montoadelantado"}, 
            {"data": "cliente"}, 
            {"data": "cliente"}, 
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {    
                    return ' <a href="#" rel="imprimiringr" class="btn btn-warning btn-xs btn-flat btnImprimir"><i class="fas fa-edit"></i></i> Impirmir</a>';           
                    // return '<a href="#" rel="imprimiringr" class="btn btn-warning btn-xs btn-flat btnImprimir"><i class="fas fa-edit"></i> Impirmir</a> ';;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return 'S/. ' + parseFloat(row.montoadelantado);
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.fechapago + ' - ' + row.horapago;
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
    
    // TABLA INGRESO COPIAS CERTIFICADAS - ACTAS
    tblIngresoCopiasCertificadas=$('#tblCopiasActas').DataTable({
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
                'action': 'listaingresocopiasacta'
            },
            dataSrc: ""
        },
        columns: [  
            {"data": "fechapago"},
            {"data": "cantidad"}, 
            {"data": "montocopias"}, 
            {"data": "cliente"}, 
            {"data": "cliente"}, 
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {               
                    return '<a href="#" rel="imprimiringcop" class="btn btn-warning btn-xs btn-flat btnImprimirCopias"><i class="fas fa-edit"></i>Impirmir</a> ';;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return 'S/. ' + parseFloat(row.montocopias);
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.fechapago + ' ' + row.horapago;
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
    
    // TABLA EGRESOS CONCILICION
    tblEgresosConciliacion=$('#tblEgresosConciliacion').DataTable({
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
                'action': 'listaegresosconciliacion'
            },
            dataSrc: ""
        },
        columns: [  
            {"data": "fechaegreso"},
            {"data": "tipinvi"},
            {"data": "montoegreso"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {               
                    return 'S/. ' + row.montoegreso;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.fechaegreso + ' ' + row.horaegreso;
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
    
    // TABLA CAJA CONCILIACION
    tblCajaConciliacion=$('#tblCajaConciliacion').DataTable({
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
                'action': 'listacajaconciliacion'
            },
            dataSrc: ""
        },
        columns: [  
            {"data": "soc.nom_per"},
            {"data": "toting_con"}, 
            {"data": "egre_con"}, 
            {"data": "id_soc"}, 
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {               
                    return 'S/. ' + (parseFloat(row.toting_con) - parseFloat(row.egre_con));
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return 'S/. ' + parseFloat(row.egre_con);
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return 'S/. ' + parseFloat(row.toting_con);
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.soc.nom_per + ' ' + row.soc.apepat_per + ' ' + row.soc.apemat_per;
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
  }

// Funcion De Inicio
$(function () { 

    getData();

    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    
    // Clientes - Ingreso Conciliacion
    var select_cliente = $('select[name="cliente"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchcliente'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_cliente.html('').select2({
                theme: "bootstrap4",
                language: "es",
                data: data
            });
            
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        //select_procedimientos.html(options);
    });
     
    // Clientes - Copias Certificadas Acta
    var select_cliente_acta = $('select[name="clienteacta"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchcliente'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_cliente_acta.html('').select2({
                theme: "bootstrap4",
                language: "es",
                data: data
            });
            
            return false;
        }
        message_error(data.error);
    }).fail(function (jqXHR, textStatus, errorThrown) {
        alert(textStatus + ': ' + errorThrown);
    }).always(function (data) {
        //select_procedimientos.html(options);
    });

    // Elemento de modal para resetearlo de Ingreso Conciliacion
    $('#modalIngresoConciliacion').on('shown.bs.modal', function(){
        // $('form')[0].reset();
    });

    // Para Agregar Ingreso Conciliacion 
    $('.btnAddIngresoConciliacion').on('click', function () {
        $('#modalIngresoConciliacion').modal('show');
    });

    // Elemento de modal para resetearlo de Ingreso Acta
    $('#modalIngresoActa').on('shown.bs.modal', function(){
        // $('form')[0].reset();
    });

    // Para Agregar Ingreso Acta 
    $('.btnAddIngresoActa').on('click', function () {
        $('#modalIngresoActa').modal('show');
    });

    // Para Agregar Egresos Conciliacion 
    $('.btnAddEgresos').on('click', function () {
        $('#modalEgresosConciliacion').modal('show');
    });

    // Para guardar el Monto de Ingreso de Conciliacion
    $('#formIngresoConciliacionDetalle').on('submit', function (e) {
        e.preventDefault();

        var montopactado = parseFloat($('input[name="montopactado"]').val());
        var montoadelanto = parseFloat($('input[name="montoadelanto"]').val());
        var montototal =  montoadelanto + parseFloat($("#id_adelanto").val());

        if(parseFloat(montototal) > parseFloat(montopactado)){
            message_error('El monto a agregar supera lo pactado, verique nuevamente');
        }else{
            var parameters = new FormData(this);
            parameters.append('action', 'ingresaringresoconciliaciondetalle');
            parameters.append('idexp', $('input[name="idexp"]').val());
            parameters.append('adelanto',$("#id_adelanto").val());
            parameters.append('cliente',$("#cliente").val());

            submit_with_ajax(window.location.pathname, 'Notificación',
                '¿Estas seguro de Agregar el Monto?', parameters, function (response) {
                    window. location. reload();
                    $('#modalIngresoConciliacion').modal('hide');
                });
            
        }

        
    });

    // Para guardar el Monto de Copias Certificadas / Acta
    $('#formIngresoActaDetalle').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'ingresocopiaacta');
        parameters.append('idexp', $('input[name="idexp"]').val());
        parameters.append('cantidadcopias',$("#id_cantidadcopias").val());
        parameters.append('montocopias',$("#id_montocopias").val());
        parameters.append('clienteacta',$("#clienteacta").val());

        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de Agregar el Monto?', parameters, function (response) {
                window. location. reload();
                $('#modalIngresoActa').modal('hide');
            });
    });

    // Para guardar Egresos Conciliacion
    $('#formEgresosConciliacion').on('submit', function (e) {
        e.preventDefault();

        var montoegresos = $('#id_montoegresos').val();

        if(montoegresos == 0 || montoegresos == null){
            message_error("Error, ingrese el dato correctamente!");
        }else{
            var parameters = new FormData(this);
            parameters.append('action', 'addegresos');
            parameters.append('idexp', $('input[name="idexp"]').val());
            parameters.append('tipoinv', $('#tipoinv').val());
            parameters.append('montoegresos',montoegresos);

            submit_with_ajax(window.location.pathname, 'Notificación',
                '¿Estas seguro de Agregar el Egreso?', parameters, function (response) {
                    window. location. reload();
                    $('#modalEgresosConciliacion').modal('hide');
                });
        }

        
    });

    // Imprimir Recibo de Ingresos conciliacion
    $('#tblIngresoDetalle tbody')
        // Imprimir
        .on('click', 'a[rel="imprimiringr"]', function () {
            var tr = tblIngresoDetalleConciliacion.cell($(this).closest('td, li')).index();
            var data = tblIngresoDetalleConciliacion.row(tr.row).data();
            window.location.href='/genreciboingresos/'+ data.iddet;
            
        })
    
    // Imprimir Recibo de Ingresos copias
    $('#tblCopiasActas tbody')
        // Imprimir
        .on('click', 'a[rel="imprimiringcop"]', function () {
            var tr = tblIngresoCopiasCertificadas.cell($(this).closest('td, li')).index();
            var data = tblIngresoCopiasCertificadas.row(tr.row).data();
            
            window.location.href='/genreciboingresoscopias/'+ data.idingcop;
        
        })
        
});