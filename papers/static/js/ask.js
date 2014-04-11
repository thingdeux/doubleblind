$(document).ready(function() {	

	//Django boilerplate functions for passing csrf cookies on POST.
	$.ajaxSetup({ 
	     beforeSend: function(xhr, settings) {
	         function getCookie(name) {
	             var cookieValue = null;
	             if (document.cookie && document.cookie != '') {
	                 var cookies = document.cookie.split(';');
	                 for (var i = 0; i < cookies.length; i++) {
	                     var cookie = jQuery.trim(cookies[i]);
	                     // Does this cookie string begin with the name we want?
	                 if (cookie.substring(0, name.length + 1) == (name + '=')) {
	                     cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
	                     break;
	                 }
	             }
	         }
	         return cookieValue;
	         }
	         if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
	             // Only send the token to relative URLs i.e. locally.
	             xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	         }
	     } 
	});



	//Instantiate jqueryUI tab
	$( "#ask_window" ).tabs();

	/*   -----  Button Handlers ----- */

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

	//Stop enter key fromPOSTING
	$('.submission_button').keypress(function (event) {
	  if (event.which == 13) {
	    event.preventDefault();
	  }
	});

	$(".submission_button").click(function (event){
		event.preventDefault();

		
		$.ajax({
			type: "POST",
			url: "/queueQuestion/",			
			data: $(this.form).serialize(),
		})
		.done(function() {
			console.log("SENT");
		})
		.fail(function() {		
			console.log("FAILED");
		});		
	});

	//Honorary button - for adding answer
	$(".add_answer").click(function (event) {
		event.preventDefault();
		console.log( $(this).closest."") );

	});


});


