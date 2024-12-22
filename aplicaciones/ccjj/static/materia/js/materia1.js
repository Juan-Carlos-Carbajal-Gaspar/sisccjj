var tblMateria;
function getData(){
    tblMateria=$('#data').DataTable({
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
                'action': 'listamateria'
            },
            dataSrc: ""
        },
        columns: [
            {"data": "id"},
            {"data": "des_mat"},
            {"data": "id"},
            
        ],
        columnDefs: [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '<a href="/materia/editarmateria/' + row.id +'/" rel="edit" class="btn btn-warning btn-xs btn-flat btnEdit"><i class="fas fa-edit"></i></a> ';
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
  
  