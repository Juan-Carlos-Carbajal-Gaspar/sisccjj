// Funcion De Inicio
$(function () { 

    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Conciliadores
    var select_conciliadores = $('select[name="conciliadores"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchconciliadores'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_conciliadores.html('').select2({
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

    // Elemento para guardar Esquela Conciliador
    $('#formesquelaconciliador').on('submit', function (e) {
        e.preventDefault();
        
        if ($("#conciliadores").val() == ''){
            message_error('Seleccione Conciliador')
        }else{
            var parameters = new FormData();
            parameters.append('action', $('input[name="action"]').val());
            parameters.append('idexp', $('input[name="idexp"]').val());
            parameters.append('conciliador',$("#conciliadores").val());
                    
            // alert(parameters.get('especificaciones'));
        
            submit_with_ajax(
                window.location.pathname, 
                'Notificación',
                '¿Estas seguro de guardar y generar el Esquela de Conciliador?', 
                parameters, function (response) {
                    // Para Generar Documento Word
                    window.location.href='/genesquelaconciliador/'+ parameters.get('idexp') + '/';
                    // // Para redireccionar a Expediente Detalles  
                    setTimeout("location.href = '/expediente/expedientedetalle/"+parameters.get('idexp')+"/';",200);
                    
                }
            );
        }
        
        
    });
    
       
        
   


})

