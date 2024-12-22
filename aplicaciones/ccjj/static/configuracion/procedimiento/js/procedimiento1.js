// Declaramos variable tblmateria para la tabla de datos
var tblprocedimiento;
function getData(){
    tbltblprocedimiento=$('#data').DataTable({
        responsive: true,
        lengthChange: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        // buttons: [ 'excel', 'pdf'],
        // dom: 'Blfrtip',
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'readprocedimiento'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "mat.des_mat"},
            {"data": "des_pro"},
            {"data": "des_pro"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/aplicacionweb/procedimiento/editar/' + row.id + '/" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                    buttons += ' <a href="/aplicacionweb/procedimiento/eliminar/' + row.id + '/" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
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

});
  
  