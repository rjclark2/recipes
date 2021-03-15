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
	{"data": "Author"},
	{"data": "Instructions"},
	{"data": "Total Time"},
	{"data": "Preperation Time"},
	{"data": "Cooking Time"},
	{"data": "Number of Servings"},
	{"data": "Calories per Serving"},
	{"data": "Fat per Serving"},
	{"data": "Carbohydrates per Serving"},
	{"data": "Protein per Serving"},
	{"data": "Cholesterol per Serving"},
	{"data": "Sodium per Serving"},
	{"data": "Number of Ratings"},
	{"data": "Average Rating"}
    ],
   "order":[[16,'desc']],
   "columnDefs":[
	          { orderable: false, targets: [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,17] },
		  {
			  "targets": [ 1 ],
			  "visible": false
		  },
	          {
                          "targets": [ 3 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 4 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 5 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 7 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 8 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 9 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 11 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 12 ],
                          "visible": false
                  },
	          {
                          "targets": [ 13 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 14 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 15 ],
                          "visible": false
                  },
 		  {
                          "targets": [ 17 ],
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

});
