// Funcion De Inicio
$(function () { 
    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    
    // Clientes
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
    
    // Elemento de modal para resetearlo de Socio
    $('#modalSocio').on('shown.bs.modal', function(){
        // $('form')[0].reset();
    });

    // Para Agregar Nuevo Socio 
    $('.btnAddSocio').on('click', function () {
        $('#modalSocio').modal('show');
    });

    // Para guardar el nuevo Socio
    $('#formSocio').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData(this);
        parameters.append('action', 'create_socio');
        submit_with_ajax(window.location.pathname, 'Notificación',
            '¿Estas seguro de agregar al socio?', parameters, function (response) {
                alert('Socio Agregado, Procede a buscarlo');
                window. location. reload();
                $('#modalSocio').modal('hide');
            });
    });

     // Elemento para guardar Pago Expediente
     $('#formingresoexpconciliacion').on('submit', function (e) {
        e.preventDefault();

        var pactado = parseFloat($("#id_pacpag_con").val());
        var descuento = parseFloat($("#id_descuento").val());
        var adelanto = parseFloat($("#id_adelanto").val());

        if (adelanto > (pactado-descuento)) {
            message_error('El adelanto no puede ser mas que el pactado, revise nuevamente');
        }
        else{
            var parameters = new FormData();
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('idexp', $('input[name="idexp"]').val());
            parameters.append('pacpag_con',$("#id_pacpag_con").val());
            parameters.append('adelanto',$("#id_adelanto").val());
            parameters.append('descuento',$("#id_descuento").val());
            parameters.append('socios',$("#id_socios").val());
            parameters.append('cliente',$("#cliente").val());
        
            submit_with_ajax(
                window.location.pathname, 
                'Notificación',
                '¿Estas seguro de guardar el ingreso?', 
                parameters, function (response) {
                    
                    window.location.href='/expediente/expedientedetalle/'+ parameters.get('idexp') + '/';                  

                }
            );
        }

        
    });

});


