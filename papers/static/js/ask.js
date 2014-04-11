$(document).ready(function() {
	//Instantiate jqueryUI tab
	$( "#ask_window" ).tabs();

	//When user clicks on 'Example Usage'
	//Slide in helper text and remove form
	$( ".helper_button").click(function() {
		$(this).next(".helper_text").toggle("slide", 400);

		var submission_form = $(this).siblings().filter('#form_container')

		if ( submission_form.is(":visible") ) {
			//Fast hide for submission form
			$(this).html('Close')
			submission_form.hide();			
		}
		else {
			//Slow reveal for submission form. 
			//Happens after slide from helper text			
			$(this).html('Instructions')
			setTimeout(function(){
				submission_form.show(200);				
								},400);
		}
	});

	$(".submission_button").click(function (event){
		event.preventDefault();
		
		
		$.ajaxSetup({data: {
			csrfmiddlewaretoken: '{{ csrf_token }}'
		}});
		
		//csrfmiddlewaretoken

		
		$.ajax({
			type: "POST",
			url: "/queueQuestion/",			
			data: $(this),
		})
		.done(function() {
			console.log("SENT");
		}).
		fail(function() {
			
			$("html").html(json)
		});

	});

});