var tblInvitado;
function getData(){
    tblInvitado=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchdatainvitados'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "dni"},
            {"data": "invitado"},
            {"data": "ninvitacion"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    if(row.estadopro == 'act'){
                        return 'Ya tiene generado la Acta';
                    }else{
                        if (row.ninvitacion == '0'){
                            return '<a h*ref="#" rel="primerainvitacion" class="btn btn-success btn-xs btn-flat btnEdit"><i class="fas fa-file-alt"></i> Primera</a> ';
                        }
                        else if (row.ninvitacion == 'p'){
                            var fechahora = row.fechainv + 'T' + row.horainv;
                            // return fechahora.toString() + ' : ' + completarFechaHora().toString();
                            if(row.fechainv.toString() == completarFechaHora().toString()){
                                return '<a h*ref="#" rel="segundainvitacion" class="btn btn-success btn-xs btn-flat btnEdit"><i class="fas fa-file-alt"></i> Segunda</a> ';
                            }else{
                                return 'Esperar la fecha de audiencia';
                            }
                            
                        }
                        else if (row.ninvitacion == 's'){
                            return 'Ya se genero todas las invitaciones';
                        }
                        else{
                            return 'Error!';
                        }
                    }
                    
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
  }
// Array de dias y meses en letras
// Dias de la Semana
    const dias = [
        "Domingo", // 0
        "Lunes", // 1
        "Martes", // 3
        "Miercoles", // 3
        "Jueves", // 4
        "Viernes", // 5
        "Sabado", // 6
    ];
//  alert(dias[formatNumDia(fechaaudiencia)]);
// Meses del Year
// Dias de la Semana
    const meses = [
        "Enero", // 0
        "Febrero", // 1
        "Marzo", // 3
        "Abril", // 3
        "Mayo", // 4
        "Junio", // 5
        "Julio", // 6
        "Agosto", // 7
        "Septiembre", // 8
        "Octubre", // 9
        "Noviembre", // 10
        "Diciembre", // 11
    ];

// Funcion Para completar automaticamente la fecha y hora / PARA GENERAR SEGUNDA INVITACION
function completarFechaHora(){
    var fecha = new Date(); //Fecha actual
    var mes = fecha.getMonth()+1; //obteniendo mes
    var dia = fecha.getDate(); //obteniendo dia
    var ano = fecha.getFullYear(); //obteniendo año
    var hora = fecha.getHours(); //obteniendo hora
    var minutos = fecha.getMinutes(); //obteniendo minuto
    
    return ano+"-"+minTwoDigits(mes)+"-"+minTwoDigits(dia);
    
  } 

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

// Para validar Fecha de Audiencia para 3 dias
function validarFechaAudiencia(fecha, cantdias) {
    var arrFecha = fecha.split('-');
    var fecha = new Date(arrFecha[0], arrFecha[1] - 1, arrFecha[2]);
    var festivos = [ // Agregamos los festivos (dia, mes)
        // dia, mes    
        [15, 4],
        [1, 5],
        [29, 6],
        [28, 7],
        [29, 7],
        [30, 8],
        [8, 10],
        [1, 11],
        [8, 12],
        [9, 12],
        [25, 12]
    ];

    for (var i = 0; i < cantdias; i++) {
        var diaInvalido = false;
        fecha.setDate(fecha.getDate() + 1); // Sumamos de dia en dia
        for (var j = 0; j < festivos.length; j++) { // Verificamos si el dia + 1 es festivo
            var mesDia = festivos[j];
            if (fecha.getMonth() + 1 == mesDia[1] && fecha.getDate() == mesDia[0]) {
                console.log(fecha.getDate() + ' es dia festivo (Sumamos un dia)');
                diaInvalido = true;
                break;
            }
        }
        if (fecha.getDay() == 0 || fecha.getDay() == 6) { // Verificamos si es sábado o domingo
            console.log(fecha.getDate() + ' es sábado o domingo (Sumamos un dia)');
            diaInvalido = true;
        }
        if (diaInvalido)
            cantdias++; // Si es fin de semana o festivo le sumamos un dia
    }
    return fecha.getFullYear() + '-' + (fecha.getMonth() + 1).toString().padStart(2, '0') + '-' + fecha.getDate().toString().padStart(2, '0');
}

function generarFechaHoraInvitacion() {
    // Iniciamos valores de invitacion
    $.ajax({
        url:   window.location.pathname,
        method: 'POST',
        data:  {
        'action': 'buscardatosinvitacion',
        },
        success: function(data)            
        {
            var numinvi = data[0];
            var fecha = data[1];
            var hora = data[2];

            if(numinvi == "p"){
                document.getElementById('lbltxtfecha').innerHTML= 'Primera Fecha de Audiencia';
                document.getElementById('lbltxthora').innerHTML= 'Hora de Audiencia';
            }else if(numinvi == "s"){
                document.getElementById('lbltxtfecha').innerHTML= 'Segunda Fecha de Audiencia';
                document.getElementById('lbltxthora').innerHTML= 'Hora de Audiencia';
            }else{
                document.getElementById('lbltxtfecha').innerHTML= '...';
                document.getElementById('lbltxthora').innerHTML= '...';
            }
                        
            $("#txtnuminvi").val(numinvi);
            $("#txtfecha").val(fecha);
            $("#txthora").val(hora);
        }
    });
}
$(function () {
    // Iniciamos variables de fecha y hora invitacion
    generarFechaHoraInvitacion();

    //Para Fecha y Hora
    $('#reservationdatetime').datetimepicker({ icons: { time: 'far fa-clock' } });

    // Para la etiqueta html
    modal_title=$('.modal-title');
      
    // Para Cargar los datos a la tabla
    getData();

    // Elemento de modal para resetearlo
    $('#modalPrimeraInvitacion').on('shown.bs.modal', function(){
        //$('form')[0].reset();
    });

    // Elemento para guardar en modal la Primera Invitacion/
    $('#formPrimeraInvitacion').on('submit', function (e) {
        e.preventDefault();
        // Fecha Hoy General
        var fechahoy = new Date();
        var fechaaudiencia = new Date($("#txtfechahora").val());
        var hora = parseInt(fechaaudiencia.getHours());
        var minutos = parseInt(fechaaudiencia.getMinutes());    
        
        // Numero de Dia de la Semana de Audiencia
        const formatNumDiaAudiencia = (fechaaudiencia)=>{
            let formatted_fechaaudiencia = fechaaudiencia.getDay();
            return formatted_fechaaudiencia;
        }

        // Formato General de Fecha Audiencia Para Documento
        const formatDateAudienciaDoc = (fechaaudiencia)=>{
            var datofecha='el día ' + dias[fechaaudiencia.getDay()] 
            + ' ' + minTwoDigits(fechaaudiencia.getDate()) + ', de '
            + meses[(fechaaudiencia.getMonth() + 1)]
            + ', a horas ' + minTwoDigits(fechaaudiencia.getHours())
            + ':' + minTwoDigits(fechaaudiencia.getMinutes());
            return datofecha;
        }

        // Formato General de Hoy Fecha
        const formatDateHoy = (fechahoy)=>{
            let formatted_fechahoy = fechahoy.getFullYear() + "-" + minTwoDigits((fechahoy.getMonth() + 1)) + "-" + minTwoDigits(fechahoy.getDate())
            return formatted_fechahoy;
        }

        // Formato General de Fecha Audiencia
        const formatDateAudiencia = (fechaaudiencia)=>{
            let formatted_fechaaudiencia = fechaaudiencia.getFullYear() + "-" + minTwoDigits((fechaaudiencia.getMonth() + 1)) + "-" + minTwoDigits(fechaaudiencia.getDate())
            return formatted_fechaaudiencia;
        }

        const formatDate = (fechaaudiencia)=>{
            let formatted_fechaaudiencia = fechaaudiencia.getFullYear() + "-" + minTwoDigits((fechaaudiencia.getMonth() + 1)) + "-" + minTwoDigits((fechaaudiencia.getDate()+1))
            return formatted_fechaaudiencia;
        }

        if (formatDateAudiencia(fechaaudiencia) < formatDateHoy(fechahoy) ){
            message_error('La fecha de Audiencia no puede ser días anteriores a la fecha actual');
            return false;
        }
        else if(formatDateAudiencia(fechaaudiencia) == formatDateHoy(fechahoy)){
            message_error('La fecha para la Audiencia no puede ser hoy, debe ser 3 días hábiles después');
            return false;
        }else{
            if (formatNumDiaAudiencia(fechaaudiencia) == 0 || formatNumDiaAudiencia(fechaaudiencia) == 6 ){
                message_error('La Audiencia no puede ser programada para los días Sabado y Domingo, eliga ofra fecha');
                return false;
            }else{
                var nuevaFecha = validarFechaAudiencia(formatDateHoy(fechahoy), 4);

                if (formatDateAudiencia(fechaaudiencia) >= nuevaFecha){
                    ///
                    if(hora > 7 && hora < 19 ){
                        if(hora == 18 && minutos > 0){
                            message_error('La hora de audiencia no puede ser programados más de las 06:00 pm');
                        }else{
                            // Validar fecha audiencia con fecha de invitacion
                            if ($("#txtfecha").val() == '' && $("#txthora").val() == ''){
                                
                                // var parameters = $(this).serializeArray();
                                var parameters = new FormData(this);
                                submit_with_ajax(
                                    window.location.pathname, 
                                    'Notificación', 
                                    '¿Estas seguro de Guardar los Datos de Primera Invitación?', 
                                    parameters, 
                                    function () {
                                        $('#modalPrimeraInvitacion').modal('hide');

                                        // Para Generar Documento Word
                                        var idexp = $("#idexp").val();
                                        var idper = $("#idper").val();
                                        
                                        window.location.href='/genpriinvitacion/'+ idexp + '/' + idper + '/' + formatDateAudienciaDoc(fechaaudiencia);
                                        
                                        tblInvitado.ajax.reload();
                                        getData();

                                        // Actualizamos variables de fecha y hora invitacion
                                        generarFechaHoraInvitacion();
                                        
                                });

                            }else{
                                var fechaaudienciainvitacion = new Date($("#txtfecha").val().toString() +' ' +$("#txthora").val().toString());
                                var horaaudiencia = fechaaudienciainvitacion.getHours() + ':' + fechaaudienciainvitacion.getMinutes();
                                var horaactual = fechaaudiencia.getHours() + ':' + fechaaudiencia.getMinutes();
                                
                                if ($("#txtfecha").val() == formatDateAudiencia(fechaaudiencia) && horaaudiencia == horaactual){
                                    // var parameters = $(this).serializeArray();
                                    var parameters = new FormData(this);
                                    submit_with_ajax(
                                        window.location.pathname, 
                                        'Notificación', 
                                        '¿Estas seguro de Guardar los Datos de Primera Invitación?', 
                                        parameters, 
                                        function () {
                                            $('#modalPrimeraInvitacion').modal('hide');

                                            // Para Generar DOcumento Word
                                            var idexp = $("#idexp").val();
                                            var idper = $("#idper").val();
                                            
                                            window.location.href='/genpriinvitacion/'+ idexp + '/' + idper + '/' + formatDateAudienciaDoc(fechaaudiencia);
                                            
                                            tblInvitado.ajax.reload();
                                            getData();

                                            // Actualizamos variables de fecha y hora invitacion
                                            generarFechaHoraInvitacion();
                                            
                                    });
                                }
                                else{
                                    message_error('La fecha y hora no coinciden, verifique nuevamente!');
                                }
                            }
                        }
                        
                    }else{
                        message_error('La hora de audiencia debe ser entre: 08:00 am - 06:00 pm');
                    } 
                    ////
                }else{
                    message_error('La Audiencia debe ser después de 3 dias habiles, eliga otra fecha');
                    return false;
                } 
                
    
            }
        }  
        
    });

    // Elemento para guardar en modal la Segunda Invitacion/
    $('#formSegundaInvitacion').on('submit', function (e) {
        e.preventDefault();
        // Fecha Hoy General
        var fechahoy = new Date();
        var fechaaudiencia = new Date($("#txtfechahoras").val());
        var hora = parseInt(fechaaudiencia.getHours());
        var minutos = parseInt(fechaaudiencia.getMinutes()); 
        
        // Numero de Dia de la Semana de Audiencia
        const formatNumDiaAudiencia = (fechaaudiencia)=>{
            let formatted_fechaaudiencia = fechaaudiencia.getDay();
            return formatted_fechaaudiencia;
        }

        // Formato General de Fecha Audiencia Para Documento
        const formatDateAudienciaDoc = (fechaaudiencia)=>{
            var datofecha='el día ' + dias[fechaaudiencia.getDay()] 
            + ' ' + minTwoDigits(fechaaudiencia.getDate()) + ', de '
            + meses[(fechaaudiencia.getMonth() + 1)]
            + ', a horas ' + minTwoDigits(fechaaudiencia.getHours())
            + ':' + minTwoDigits(fechaaudiencia.getMinutes());
            return datofecha;
        }

        // Formato General de Hoy Fecha
        const formatDateHoy = (fechahoy)=>{
            let formatted_fechahoy = fechahoy.getFullYear() + "-" + minTwoDigits((fechahoy.getMonth() + 1)) + "-" + minTwoDigits(fechahoy.getDate())
            return formatted_fechahoy;
        }

        // Formato General de Fecha Audiencia
        const formatDateAudiencia = (fechaaudiencia)=>{
            let formatted_fechaaudiencia = fechaaudiencia.getFullYear() + "-" + minTwoDigits((fechaaudiencia.getMonth() + 1)) + "-" + minTwoDigits(fechaaudiencia.getDate())
            return formatted_fechaaudiencia;
        }

        const formatDate = (fechaaudiencia)=>{
            let formatted_fechaaudiencia = fechaaudiencia.getFullYear() + "-" + minTwoDigits((fechaaudiencia.getMonth() + 1)) + "-" + minTwoDigits((fechaaudiencia.getDate()+1))
            return formatted_fechaaudiencia;
        }

        if (formatDateAudiencia(fechaaudiencia) < formatDateHoy(fechahoy) ){
            message_error('La fecha para la Segunda Audiencia no puede ser días anteriores a la fecha actual');
            return false;
        }
        else if(formatDateAudiencia(fechaaudiencia) == formatDateHoy(fechahoy)){
            message_error('La fecha para la Segunda Audiencia no puede ser hoy, debe ser 3 días hábiles despues');
            return false;
        }else{
            if (formatNumDiaAudiencia(fechaaudiencia) == 0 || formatNumDiaAudiencia(fechaaudiencia) == 6 ){
                message_error('La Audiencia no puede ser programada para los días Sabado y Domingo, eliga ofra fecha');
                return false;
            }else{
                var nuevaFecha = validarFechaAudiencia(formatDateHoy(fechahoy), 4);

                if (formatDateAudiencia(fechaaudiencia) >= nuevaFecha){
                    
                    ///
                    if(hora > 7 && hora < 19 ){
                        if(hora == 18 && minutos > 0){
                            message_error('La hora de audiencia no puede ser programados más de las 06:00 pm');
                        }else{
                            // Validar Numero de Invitacion (Primera o Segunda)
                            if ($("#txtnuminvi").val() == 'p'){
                                
                                // var parameters = $(this).serializeArray();
                                var parameters = new FormData(this);
                                submit_with_ajax(
                                    window.location.pathname, 
                                    'Notificación', 
                                    '¿Estas seguro de Guardar los Datos de Segunda Invitación?', 
                                    parameters, 
                                    function () {
                                        $('#modalSegundaInvitacion').modal('hide');

                                        // Para Generar Documento Word
                                        var idexp = $("#idexps").val();
                                        var idper = $("#idpers").val();
                                        
                                        window.location.href='/genseginvitacion/'+ idexp + '/' + idper + '/' + formatDateAudienciaDoc(fechaaudiencia);
                                        
                                        tblInvitado.ajax.reload();
                                        getData();

                                        // Actualizamos variables de fecha y hora invitacion
                                        generarFechaHoraInvitacion();
                                        
                                });

                            }else{
                                var fechaaudienciainvitacion = new Date($("#txtfecha").val().toString() +' ' +$("#txthora").val().toString());
                                var horaaudiencia = fechaaudienciainvitacion.getHours() + ':' + fechaaudienciainvitacion.getMinutes();
                                var horaactual = fechaaudiencia.getHours() + ':' + fechaaudiencia.getMinutes();
                                
                                if ($("#txtfecha").val() == formatDateAudiencia(fechaaudiencia) && horaaudiencia == horaactual){
                                    // var parameters = $(this).serializeArray();
                                    var parameters = new FormData(this);
                                    submit_with_ajax(
                                        window.location.pathname, 
                                        'Notificación', 
                                        '¿Estas seguro de Guardar los Datos de Segunda Invitación?', 
                                        parameters, 
                                        function () {
                                            $('#modalSegundaInvitacion').modal('hide');

                                            // Para Generar DOcumento Word
                                            var idexp = $("#idexps").val();
                                            var idper = $("#idpers").val();
                                            
                                            window.location.href='/genseginvitacion/'+ idexp + '/' + idper + '/' + formatDateAudienciaDoc(fechaaudiencia);
                                            
                                            tblInvitado.ajax.reload();
                                            getData();

                                            // Actualizamos variables de fecha y hora invitacion
                                            generarFechaHoraInvitacion();
                                            
                                    });
                                }
                                else{
                                    message_error('La fecha y hora no coinciden, verifique nuevamente!');
                                }
                            }
                        }
                        
                    }else{
                        message_error('La hora de audiencia debe ser entre: 08:00 am - 06:00 pm');
                    } 
                    ////

                }else{
                    message_error('La Audiencia debe ser despues de 3 días hábiles, eliga otra fecha');
                    return false;
                } 
    
            }
        }  
    });

    // Para generar primera invitacion
    $('#data tbody')
        // Editar Primera Invitacion
        .on('click', 'a[rel="primerainvitacion"]', function () {
            modal_title.find('span').html('Establecer Fecha y Hora para Primera Audiencia: ');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblInvitado.cell($(this).closest('td, li')).index();
            var data = tblInvitado.row(tr.row).data();
            $('input[name="action"]').val('addprimera');
            $('input[name="id"]').val(data.id);
            $('input[name="idper"]').val(data.idper);
            $('input[name="invitado"]').val(data.invitado);
            $('#modalPrimeraInvitacion').modal('show');
        })
        // Editar Segunda Invitacion
        .on('click', 'a[rel="segundainvitacion"]', function () {
            modal_title.find('span').html('Establecer Fecha y Hora para Segunda Audiencia: ');
            modal_title.find('i').removeClass().addClass('fas fa-edit');
            var tr = tblInvitado.cell($(this).closest('td, li')).index();
            var data = tblInvitado.row(tr.row).data();
            $('input[name="action"]').val('addsegunda');
            $('input[name="ids"]').val(data.id);
            $('input[name="idpers"]').val(data.idper);
            $('input[name="invitados"]').val(data.invitado);
            $('#modalSegundaInvitacion').modal('show');
        })
});
  
  