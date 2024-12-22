// Funcion De Inicio
$(function () { 

    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });
    
    // Elemento para guardar Acta Expediente
     $('#formactaconciliacion').on('submit', function (e) {
        e.preventDefault();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('idexp', $('input[name="idexp"]').val());
        parameters.append('numacta', $("#numacta").val());
        parameters.append('tip_inf',$("#tipacta").val());
        parameters.append('fec_inf',$("#id_fec_inf").val());
       
        submit_with_ajax(
            window.location.pathname, 
            'Notificación',
            '¿Estas seguro de guardar y generar la Acta?', 
            parameters, function (response) {
                // Para Generar DOcumento Word
                window.location.href='/generaracta/'+ parameters.get('idexp');
                // window.history.back(); 
                // Para redireccionar a expediente detalle
                setTimeout("location.href = '/expediente/expedientedetalle/"+ parameters.get('idexp') + "/';",300);
            }
        );
    });

});


