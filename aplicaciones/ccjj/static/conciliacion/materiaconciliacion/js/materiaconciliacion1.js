function selectMateriaConciliacion() {
    var select_procedimientos = $('select[name="procedimientos"]');
    var select_especificaciones = $('select[name="especificaciones"]');     
    $('.select2').select2({
        theme: "bootstrap4",
        language: "es",
    });
    // Procedimientos
    $('select[name="materias"]').on('change', function () {
            var id = $(this).val();
            var options = '<option value="">--------------</option>';
            if (id === '') {
                select_procedimientos.html(options);
                return false;
            }
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_procedimientos_id',
                    'id': id
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    // Utilizando la libreria de select2
                    select_procedimientos.html('').select2({
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
        });   
        
        // especificaciones
        $('select[name="procedimientos"]').on('change', function () {
            var id = $(this).val();
            var options = '<option value="">--------------</option>';
            if (id === '') {
                select_especificaciones.html(options);
                return false;
            }
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_especificaciones_id',
                    'id': id
                },
                dataType: 'json',
            }).done(function (data) {
                if (!data.hasOwnProperty('error')) {
                    // Utilizando la libreria de select2
                    select_especificaciones.html('').select2({
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
                //select_especificaciones.html(options);
            });
        });
}
    

// Funcion para que se ejecute cuando abrimos el templatte
$(function () {
    // Para seleccionar las amterias conciliables
    selectMateriaConciliacion();
    
     // Elemento para guardar materias conciliables
    $('#formmateriaconciliacion').on('submit', function (e) {
        e.preventDefault();

        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('idexp', $('input[name="idexp"]').val());
        parameters.append('materias',$("#id_materias").val());
        parameters.append('especificaciones',$("#id_especificaciones").val());
                
        // alert(parameters.get('especificaciones'));
       
        submit_with_ajax(
            window.location.pathname, 
            'Notificación',
            '¿Estas seguro de Guardar la Materia Conciliable?', 
            parameters, function (response) {
                window.location.href='/expediente/expedientedetalle/'+ parameters.get('idexp') + '/';                  
            }
        );
    });

    
});