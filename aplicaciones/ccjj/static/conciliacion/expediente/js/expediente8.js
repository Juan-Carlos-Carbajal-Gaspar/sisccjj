var tblExpediente;

function getData(){
      tblExpediente=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ordering: false,
        bAutoWidth:true,
        sScrollX:true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'listaexpediente'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "num_exp"},
            {"data": "fec_exp"},
            {"data": "tipcon_exp"},
            {"data": "confin_exp"},
            {"data": "num_exp"},

        ],
        columnDefs: [
            {
                targets: [-5], // Numero Expediente
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var fecyear = new Date(row.fec_exp);
                    var year = fecyear.getFullYear();
                    return row.num_exp + " - " + year;
                }
            },
            {
                targets: [-4], // Fecha y Hora
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return row.fec_exp + ' - ' + row.hor_exp;
                }
            },
            {
                targets: [-3], // Tipo de Conciliacion
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(row.tipcon_exp=='ma'){
                        return '<span class="badge badge-success">MISMO ACTO</span> ';
                    }
                    return '<span class="badge badge-warning">CON INVITACIÓN</span> ';
                }
            },
            {
                targets: [-2], // Finalizado/No Finalizado de Conciliacion
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    if(row.confin_exp=='FINALIZADO'){
                        return '<span class="badge badge-info">FINALIZADO</span> ';
                    }
                    return '<span class="badge badge-danger">NO FINALIZADO</span> ';
                }
            },
            {
                targets: [-1], // Opcion Editar3
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    
                    return '<a href="#" rel="editexp" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></i> Ver</a>';
                }
            },
                        
        ],
        initComplete: function (settings, json) {
            //alert("Tabla Cargada");
        }
      });
}

$(function () {
      
    // Para Cargar los datos a la tabla
    getData();

    // -------------------------------//
    //---TABLA EXPEDIENTE-------------//
    //--------------------------------//
    // Para editar
    $('#data tbody')
        // Ver Detalle Expediente
        .on('click', 'a[rel="editexp"]', function () {
            var tr = tblExpediente.cell($(this).closest('td, li')).index();
            var data = tblExpediente.row(tr.row).data();

            window.location.href='/expediente/expedientedetalle/'+ data.id + '/';
        })
    // -------------------------------//
    //---TABLA EXPEDIENTE-------------//
    //--------------------------------//

});
  
  