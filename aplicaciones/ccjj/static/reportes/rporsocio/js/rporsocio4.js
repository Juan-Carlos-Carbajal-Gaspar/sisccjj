// Funcion Para Cargar los Filtros
function cargarFiltros(){
    // Cargar bootstrap 4 para buscadores de select
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    // Socios
    var select_socio = $('select[name="socio"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchsocio'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_socio.html('').select2({
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

    // Materias
    var select_materias = $('select[name="materias"]');
    $.ajax({
        url: window.location.pathname,
        type: 'POST',
        data: {
            'action': 'searchmaterias'
        },
        dataType: 'json',
    }).done(function (data) {
        if (!data.hasOwnProperty('error')) {
            // Utilizando la libreria de select2
            select_materias.html('').select2({
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

    // Procedimientos
    var select_procedimientos = $('select[name="procedimientos"]');    
    $('select[name="materias"]').on('change', function () {
            var id = $(this).val();
            var options = '<option value="all">Todos</option>';
            if (id === 'all') {
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
}


var tblReportePorSocio;
// Cargar datos con resultado Todos
function getDataReportePorSocioAll(){
    tblReportePorSocio=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchreporteall'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "numexp"},
            {"data": "solicitante"},
            {"data": "invitado"},
            {"data": "fechsoli"},
            {"data": "materia"},
            {"data": "numacta"},
            {"data": "numinforme"},
            {"data": "tipacta_acta"},
            {"data": "condecono"},
        ],
        columnDefs: [
            
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.condecono == ''){
                        resp='Sin dato';
                    }
                    else{
                        resp=row.condecono;
                    }

                    return resp;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.tipacta_acta == 'at'){
                        resp='Acuerdo Total';
                    }
                    else if(row.tipacta_acta=='ap'){
                        resp='Acuerdo Parcial';
                    }
                    else if(row.tipacta_acta=='fa'){
                        resp='Falta De Acuerdo';
                    }
                    else if(row.tipacta_acta=='is'){
                        resp='Inasistencia Solicitante';
                    }
                    else if(row.tipacta_acta=='ii'){
                        resp='Inasistencia Invitado';
                    }
                    else if(row.tipacta_acta=='iap'){
                        resp='Inasistencia de Ambas Partes';
                    }
                    else if(row.tipacta_acta=='am'){
                        resp='Acta Motivada';
                    }
                    else if(row.tipacta_acta=='ci'){
                        resp='Conclusion Con Informe';
                    }
                    else{
                        resp='Sin Acta';
                    }

                    return resp;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.numinforme == ''){
                        resp='Sin Informe';
                    }
                    else{
                        resp=row.numinforme;
                    }

                    return resp;
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.numacta == ''){
                        resp='Sin Acta';
                    }
                    else{
                        resp=row.numacta;
                    }

                    return resp;
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.materia + " / " + row.procedimiento;
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var res = "";
                    if(row.fechsoli == ""){
                        res = "Sin fecha";
                    }else{
                        res = row.fechsoli
                    }
                    return res;
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var res = "";
                    if(row.invitado == ""){
                        res = "Sin invitados";
                    }else{
                        res = row.invitado
                    }
                    return res;
                }
            },
            {
                targets: [-8],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var res = "";
                    if(row.solicitante == ""){
                        res = "Sin solicitantes";
                    }else{
                        res = row.solicitante
                    }
                    return res;
                }
            },
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
  }

// Cargar datos con resultado de Filtros
function getDataReportePorSocioFiltro(socio, materia, procedimiento, fechdesde, fechhasta, tipacta){
    tblReportePorSocio=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'searchreportefiltro',
                'socio': socio,
                'materia': materia,
                'fechdesde': fechdesde,
                'fechhasta': fechhasta,
                'procedimiento': procedimiento,
                'tipacta': tipacta
            },
            dataSrc: ""
        },
        columns: [
            {"data": "numexp"},
            {"data": "solicitante"},
            {"data": "invitado"},
            {"data": "fechsoli"},
            {"data": "materia"},
            {"data": "numacta"},
            {"data": "numinforme"},
            {"data": "tipacta_acta"},
            {"data": "condecono"},
        ],
        columnDefs: [
            
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.condecono == ''){
                        resp='Sin dato';
                    }
                    else{
                        resp=row.condecono;
                    }

                    return resp;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.tipacta_acta == 'at'){
                        resp='Acuerdo Total';
                    }
                    else if(row.tipacta_acta=='ap'){
                        resp='Acuerdo Parcial';
                    }
                    else if(row.tipacta_acta=='fa'){
                        resp='Falta De Acuerdo';
                    }
                    else if(row.tipacta_acta=='is'){
                        resp='Inasistencia Solicitante';
                    }
                    else if(row.tipacta_acta=='ii'){
                        resp='Inasistencia Invitado';
                    }
                    else if(row.tipacta_acta=='iap'){
                        resp='Inasistencia de Ambas Partes';
                    }
                    else if(row.tipacta_acta=='am'){
                        resp='Acta Motivada';
                    }
                    else if(row.tipacta_acta=='ci'){
                        resp='Conclusion Con Informe';
                    }
                    else{
                        resp='Sin Acta';
                    }

                    return resp;
                }
            },
            {
                targets: [-3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.numinforme == ''){
                        resp='Sin Informe';
                    }
                    else{
                        resp=row.numinforme;
                    }

                    return resp;
                }
            },
            {
                targets: [-4],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var resp='';

                    if(row.numacta == ''){
                        resp='Sin Acta';
                    }
                    else{
                        resp=row.numacta;
                    }

                    return resp;
                }
            },
            {
                targets: [-5],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.materia + " / " + row.procedimiento;
                }
            },
            {
                targets: [-6],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var res = "";
                    if(row.fechsoli == ""){
                        res = "Sin fecha";
                    }else{
                        res = row.fechsoli
                    }
                    return res;
                }
            },
            {
                targets: [-7],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var res = "";
                    if(row.invitado == ""){
                        res = "Sin invitados";
                    }else{
                        res = row.invitado
                    }
                    return res;
                }
            },
            {
                targets: [-8],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var res = "";
                    if(row.solicitante == ""){
                        res = "Sin solicitantes";
                    }else{
                        res = row.solicitante
                    }
                    return res;
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
    // Cargar Filtros
    cargarFiltros();

    // Cargar datos resultados Todos
    getDataReportePorSocioAll();

    // Boton Buscar por Filtros
    $('.btnSearch').on('click', function () {

        // Capturo mis filtros
        var socio = $('#socio').val();
        var materia = $('#materias').val();
        var procedimiento = $('#procedimientos').val();
        var fechdesde = $('#fechdesde').val();
        var fechhasta = $('#fechhasta').val();
        var tipacta = $('#acta').val();
        
        if (fechdesde == '' || fechhasta == ''){
            message_error('Debe definir un rango de fecha');
            return false;   
        }
        else{
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'searchdatossocio',
                    'id': socio
                },
                success:  function (data) {
                    // console.log(JSON.stringify(data));
                    $("#resdni").val(data[0] + ' - ' + data[1]);
                    if (tipacta == 'all'){
                        $("#resacta").val('Acta: Todos');
                    }else if(tipacta == 'CI'){
                        $("#resacta").val('Acta: CONCLUIDO CON INFORME');
                    }else if(tipacta == 'CA'){
                        $("#resacta").val('Acta: CONCLUIDO CON ACTA');
                    }else{
                        $("#resacta").val('Acta: NINGUNA');
                    }
                    $("#resfecha").val('Desde: ' + fechdesde + ' - ' + fechhasta);
                    $("#data tbody tr").remove();
                    
                    getDataReportePorSocioFiltro(socio, materia, procedimiento, fechdesde, fechhasta, tipacta);                    
                    
                }
            });
        
            
        }
    
      });

})

