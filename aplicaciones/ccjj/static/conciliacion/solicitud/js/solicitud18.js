// TABLA DE LOS SOLICITANTES AGREGADOS PARA EXPEDIENTE-INICIO
var tblSolicitante;
var solicitante = {
    items: {
        exp: '',
        perssol: '',
        solicitantes: []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.solicitantes, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.solicitantes.push(item);
        this.list();
    },
    list: function () {
        tblSolicitante = $('#tblSolicitante').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            search: false,
            searching: false,
            paging: false,
            bInfo: false,
            data: this.items.solicitantes,
            columns: [
                {"data": "id_per"},
                {"data": "full_name"},
                {"data": "per.numcel_per"},
                {"data": "per.dir_per"},
                {"data": "per.ema_per"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="editsol" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a rel="removesol" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        console.clear();
        console.log(this.items);
        console.log(this.get_ids());
    },
};
// TABLA DE LOS SOLICITANTES AGREGADOS PARA EXPEDIENTE-FIN

 // TABLA DE LOS INVITADOS AGREGADOS PARA EXPEDIENTE-INICIO
 var tblInvitado;
 var invitado = {
     items: {
         exp: '',
         perssol: '',
         invitados: []
     },
     get_ids: function () {
         var ids = [];
         $.each(this.items.invitados, function (key, value) {
             ids.push(value.id);
         });
         return ids;
     },
     add: function (item) {
         this.items.invitados.push(item);
         this.list();
     },
     list: function () {
         tblInvitado = $('#tblInvitado').DataTable({
             responsive: true,
             autoWidth: false,
             destroy: true,
             deferRender: true,
             search: false,
             searching: false,
             paging: false,
             bInfo: false,
             data: this.items.invitados,
             columns: [
                {"data": "id_per"},
                {"data": "full_name"},
                {"data": "per.numcel_per"},
                {"data": "per.dir_per"},
                {"data": "per.ema_per"},
             ],
             columnDefs: [
                 {
                     targets: [0],
                     class: 'text-center',
                     orderable: false,
                     render: function (data, type, row) {
                         var buttons = '<a rel="editinv" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                         buttons += '<a rel="removeinv" class="btn btn-danger btn-xs btn-flat" style="color: white;"><i class="fas fa-trash-alt"></i></a>';
                         return buttons;
                     }
                 },
             ],
             initComplete: function (settings, json) {

             }
         });
         console.clear();
         console.log(this.items);
         console.log(this.get_ids());
     },
 };
// // TABLA DE LOS INVITADOS AGREGADOS PARA EXPEDIENTE-FIN



// Funcion De Inicio
$(function () {
    
    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

     // VALIDACION DE DATOS CLIENTE - INICIO
    // Para validar Numero de DNi
    $('input[name="numdoc_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
            event.preventDefault();
            return false;
        }
    });

    // Para validar Edad
    $('input[name="eda_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
            event.preventDefault();
            return false;
        }
    });

    // Para validar Numero de celular
    $('input[name="numcel_per"]').bind('keypress', function(event) {
        var regex = new RegExp("^[0-9]+$");
        var key = String.fromCharCode(!event.charCode ? event.which : event.charCode);
        if (!regex.test(key)) {
          event.preventDefault();
          return false;
        }
    });

    // VALIDACION DE DATOS CLIENTE - FIN

    // Para la etiqueta html
    modal_title=$('.modal-title');
       
    // CREAR NUEVO CLIENTE COMO SOLICITANTE - INICIO

    // Abrir Modal
    
    $('.btnAddSolicitante').on('click', function () {
        modal_title.find('span').html('Agregar Nuevo Solicitante');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        
        $('#modalSolicitantes').modal('show');
        $('#formSolicitantes')[0].reset()
    });

    // Para guardar el nuevo cliente
    $('#formSolicitantes').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        //parameters.append('action', 'create_cliente');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar datos del Solicitante?', parameters, function (response) {
                alert('Datos Guardados, Procede a Buscarlo');
                // var newOption = new Option(response.full_name,response.id, false, true);
                // $('select[name="searchsol"]').append(newOption).trigger('change');
                $('#modalSolicitantes').modal('hide');
            });
    });
    // CREAR NUEVO CLIENTE COMO SOLICITANTE - FIN

    // CREAR NUEVO CLIENTE COMO INVITADO - INICIO

    // Abrir Modal
    
    $('.btnAddInvitado').on('click', function () {
        modal_title.find('span').html('Agregar Nuevo Invitado');
        console.log(modal_title.find('i'));
        modal_title.find('i').removeClass().addClass('fas fa-plus');
        
        $('#modalInvitados').modal('show');
        $('#formInvitados')[0].reset()
    });

    // Para guardar el nuevo cliente
    $('#formInvitados').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        //parameters.append('action', 'create_cliente');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de guardar datos del Invitado?', parameters, function (response) {
                alert('Datos Guardados, Procede a Buscarlo');
                // var newOption = new Option(response.full_name,response.id, false, true);
                // $('select[name="searchsol"]').append(newOption).trigger('change');
                $('#modalInvitados').modal('hide');
            });
    });
    // CREAR NUEVO CLIENTE COMO INVITADO - FIN

    // // BUSCAR Y AGREGAR SOLICITANTE-INICIO

    // Buscar Solicitantes
    $('select[name="searchsol"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_cliente'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese DNI Solicitante',
        minimumInputLength: 1,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
          
        solicitante.add(data);        
        $(this).val('').trigger('change.select2');
        
    });

    // Limpiar todo
    $('.btnRemoveAllSol').on('click', function () {
        if (solicitante.items.solicitantes.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu lista?', function () {
            // solicitante.items.solicitantes = [];
            // solicitante.list();
            window.location.href='/expediente/expedientesolicitud/'+ $('input[name="idexpediente"]').val() + '/';
        }, function () {

        });
    });

    // Limpiar un registro
    $('#tblSolicitante tbody')
        // Editar datos Solicitante
        .on('click', 'a[rel="editsol"]', function () {
            modal_title.find('span').html('Editar datos del Solicitante');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblSolicitante.cell($(this).closest('td, li')).index();
            var data = tblSolicitante.row(tr.row).data();
            $('input[name="action"]').val('editar_cliente');
            $('input[name="id"]').val(data.per.id);
            $('input[name="numdoc_per"]').val(data.per.numdoc_per);
            $('input[name="nom_per"]').val(data.per.nom_per);
            $('input[name="apepat_per"]').val(data.per.apepat_per);
            $('input[name="apemat_per"]').val(data.per.apemat_per);
            $('input[name="eda_per"]').val(data.per.eda_per);
            $('select[name="sex_per"]').val(data.per.sex_per.id);
            $('input[name="dir_per"]').val(data.per.dir_per);
            $('input[name="numcel_per"]').val(data.per.numcel_per);
            $('input[name="ema_per"]').val(data.per.ema_per);
            $('#modalSolicitantes').modal('show');

        })
        // Eliminar datos Solicitante
        .on('click', 'a[rel="removesol"]', function () {
            var tr = tblSolicitante.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el solicitante de tu lista?',
                function () {
                    solicitante.items.solicitantes.splice(tr.row, 1);
                    solicitante.list();
                }, function () {

                });
        });

    // BUSCAR Y AGREGAR SOLICITANTE-FIN


    // // BUSCAR Y AGREGAR INVITADO-INICIO

    // Buscar Invitados
    $('select[name="searchinv"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_cliente'
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese DNI Invitado',
        minimumInputLength: 1,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        invitado.add(data);
        $(this).val('').trigger('change.select2');
    });

    // Limpiar todo
    $('.btnRemoveAllInv').on('click', function () {
        if (invitado.items.invitados.length === 0) return false;
        alert_action('Notificación', '¿Estas seguro de eliminar todos los items de tu lista?', function () {
            // solicitante.items.solicitantes = [];
            // solicitante.list();
            window.location.href='/expediente/expedientesolicitud/'+ $('input[name="idexpediente"]').val() + '/';
        }, function () {

        });
    });

    // Limpiar un registro
    $('#tblInvitado tbody')
        // Editar datos Invitado
        .on('click', 'a[rel="editinv"]', function () {
            modal_title.find('span').html('Editar datos del Invitado');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblInvitado.cell($(this).closest('td, li')).index();
            var data = tblInvitado.row(tr.row).data();
            $('input[name="action"]').val('editar_cliente');
            $('input[name="id"]').val(data.per.id);
            $('input[name="numdoc_per"]').val(data.per.numdoc_per);
            $('input[name="nom_per"]').val(data.per.nom_per);
            $('input[name="apepat_per"]').val(data.per.apepat_per);
            $('input[name="apemat_per"]').val(data.per.apemat_per);
            $('input[name="eda_per"]').val(data.per.eda_per);
            $('select[name="sex_per"]').val(data.per.sex_per.id);
            $('input[name="dir_per"]').val(data.per.dir_per);
            $('input[name="numcel_per"]').val(data.per.numcel_per);
            $('input[name="ema_per"]').val(data.per.ema_per);
            $('#modalSolicitantes').modal('show');

        })
        // Eliminar datos Invitado
        .on('click', 'a[rel="removeinv"]', function () {
            var tr = tblInvitado.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar el invitado de tu lista?',
                function () {
                    invitado.items.invitados.splice(tr.row, 1);
                    invitado.list();
                }, function () {

                });
        });

    // BUSCAR Y AGREGAR INVITADO-FIN

    // CREAR SOLICITUD - INICIO
    $('#formsolicitudgeneral').on('submit', function (e) {
        e.preventDefault();

        var tipoconciliacion=$('input[name="tipocon"]').val()

        if (tipoconciliacion == 'ma'){
            if (solicitante.items.solicitantes.length < 2) {
                message_error('Debe al menos tener dos partes en conflicto');
                return false;
            }
        }
        else if (tipoconciliacion == 'ci'){
            if (solicitante.items.solicitantes.length < 1) {
                message_error('Debe al menos tener un solicitante');
                return false;
            }
            if (invitado.items.invitados.length < 1) {
                message_error('Debe al menos tener un invitado');
                return false;
            } 
        }

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('fechSolicitud', $('input[name="fechSolicitud"]').val());
        parameters.append('txtHechos',$("#txtHechos").val());
        parameters.append('txtPretension',$("#txtPretension").val());
        parameters.append('solicitante', JSON.stringify(solicitante.items));
        parameters.append('invitado', JSON.stringify(invitado.items));
        parameters.append('idexp', $('input[name="idexpediente"]').val());
        // parameters.append('invitado', JSON.stringify(invitado.items));
       
        
        // alert(numexpediente);
       
        submit_with_ajax(
            window.location.pathname, 
            'Notificación',
            '¿Estas seguro de guardar y generar la Solicitud?', 
            parameters, function (response) {
                // Para Generar Documento Word
                window.location.href='/gensolicitud/' + parameters.get('idexp');
                // // Para redireccionar a Expediente Detalles  
                setTimeout("location.href = '/expediente/expedientedetalle/"+parameters.get('idexp')+"/';",300);
            }
        );
    });
    // CREAR SOLICITUD - FIN

});


