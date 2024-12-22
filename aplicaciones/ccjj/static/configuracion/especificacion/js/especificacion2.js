// Declaramos variable tblmateria para la tabla de datos
var tblespecificacion;
function getData(){
    tbltblespecificacion=$('#data').DataTable({
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
                'action': 'readespecificacion'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "pro.mat.des_mat"},
            {"data": "pro.des_pro"},
            {"data": "des_esp"},
            {"data": "cos_esp"},
            {"data": "des_esp"},
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    var buttons = '<a href="/aplicacionweb/especificacion/editar/' + row.id + '/" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
                    buttons += ' <a href="/aplicacionweb/especificacion/eliminar/' + row.id + '/" rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    return buttons;
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return "S/. " + row.cos_esp;
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
  
  