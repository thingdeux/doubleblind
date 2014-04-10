$(document).ready(function() {
	//Instantiate jqueryUI tab
	$( "#ask_window" ).tabs();

	//When user clicks on 'Example Usage'
	//Slide in helper text and remove form
	$( ".helper_button").click(function() {
		$(this).next(".helper_text").toggle("slide", 400);

		var submission_form = $(this).siblings().filter('.submission_form')

		if ( submission_form.is(":visible") ) {
			//Fast hide for submission form
			$(this).html('Close Example')
			submission_form.hide();			
		}
		else {
			//Slow reveal for submission form. 
			//Happens after slide from helper text			
			$(this).html('Show Example')
			setTimeout(function(){
				submission_form.show(200);				
								},400);
		}
	});

});