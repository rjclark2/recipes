$(document).ready(function() {
    $('#data').DataTable( {
    	"columnDefs": [
    		{
    			"targets": [1],
    			"visible": false,
    			"searchable": false
    		}
    	]
    } );
} );
