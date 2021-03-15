$(document).ready(function () {
  var table = $('#mydata').DataTable({
    
    bProcessing: true,
    bServerSide: true,
    sPaginationType: "full_numbers",
    lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
    bjQueryUI: true,
    sAjaxSource: '/tables/serverside_table',
    columns: [
	{"data": "Recipe Name"},
	{"data": "Description"},
	{"data": "Ingredients"},
	{"data": "Original Recipe Website"},
	{"data": "Instructions"},
	{"data": "Number of Ratings"},
	{"data": "Recommended"}
    ],
   "order":[[6,'desc'],[5,'desc']],
   "columnDefs":[
	          { orderable: false, targets: [1,2,3,4] },
		  {
			  "targets": [ 2 ],
			  "visible": false
		  },
	   	  {
                          "targets": [ 4 ],
                          "visible": false
                  }
	        ]
  });
$('#mydata tbody').on( 'click', 'tr', function () {
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
	}
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
	}
    } );

	$('#button').click( function () {
                $.ajax({
                        url: 'pdf',
			type: "POST",
			//dataType: 'json',
                        data: JSON.stringify(table.row('.selected').data()),
                        success: function (){ window.location.href = "pdf";},
                        error: function (xhr, ajaxOptions, thrownError) { alert("error") }
                });
	});

	$('a.toggle-vis').on( 'click', function (e) {
        e.preventDefault();
 
        // Get the column API object
        var column = table.column( $(this).attr('data-column') );
 
      // Toggle the visibility
        column.visible( ! column.visible() );
    } );
//
//	$('#button').click( function () {
//		$.ajax({
//			url: '/pdf',
//			data: JSON.stringify(table.rows('.selected').data()),
//			type: "POST",
//			dataType: 'json',
//			success: function (){ window.location.href = "/pdf";},
//			error: function (xhr, ajaxOptions, thrownError) { alert("error") }
//		});
//	$.post( "/pdf", {
//		data: table.row('.selected').data().//, success: function (){ window.location.href = "/pdf";}
//	});
//    } );
//
});
