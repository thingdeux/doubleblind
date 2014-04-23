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
	$(".helper_button").click(function() {
		$(this).next(".helper_text").toggle("slide", 400);
		

		var submission_form = $(this).siblings().filter('#form_container')

		if ( submission_form.is(":visible") ) {
			//Fast hide for submission form
			$(this).html('Return')
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

	//Submit form on click of 'ask' button
	$(".submission_button").click(function (event){
		event.preventDefault();
		
		$.ajax({
			type: "POST",
			url: "/queueQuestion/",			
			data: $(this.form).serialize(),
		})
		.done(function(xhr) {
			if (xhr.status == 400) {				
				$("#errors").html(xhr.statusText)
			}
		})
		.fail(function(xhr) {					
			if (xhr.status == 400) {
				$("#errors").html(xhr.statusText)
			}
		});
	});

	//Honorary button - for adding another answer textbox
	//Bound to form for performance
	$("#multi_form").on("click", ".add_answer, .remove_answer", function (event) {				
		add_remove_buttons('.answer_text', $(this), event)		
	});

	$("#secret_form").on("click", ".add_answer, .remove_answer", function (event) {
		add_remove_buttons('.secret_answer_text', $(this), event)			
	});

	function buildNewAnswerBox(newLocation, className) {

		//Line termination \ slashes only used for readability		
		var newString = '<tr><td><input type="radio" name="selected_answer" value="' + newLocation + '"/></td><td> \
		<input type="text" size="32" class="' + className.slice(1) +'" name="answertext-' + newLocation + '" placeholder="Answer (Optional)"/></td> \
		<td class="add_answer"><span class="ui-icon ui-icon-circle-plus"></span></td> \
		<td class="remove_answer"><span class="ui-icon ui-icon-circle-minus"></span></td></tr>'			
		return (newString)
	}

	function add_remove_buttons(textBoxName, jqueryObj, jqueryEvent) {
		if (jqueryEvent.currentTarget.className == "add_answer") {
			//Get the name from the answer input box, increment the number following the -
			//Add a new textbox below it with the next number
			var lastAnswer = jqueryObj.siblings().find(textBoxName).attr('name');
			var answerName = parseInt(lastAnswer.slice(11, lastAnswer.length)  );
			var answerCount = $(textBoxName).length			
			
			//Hide all add buttons if there are 10 answer boxes on screen - 10 is plenty.			
			if (answerCount + 1 <= 10) {
				$(buildNewAnswerBox(answerName + 1, textBoxName)).insertAfter( jqueryObj.parent() );			
				jqueryObj.hide();
				//Remove last add_answer button
				if (answerCount + 1 == 10) {
					$('.add_answer').hide();
				}
			}			
		}
		else if (jqueryEvent.currentTarget.className == "remove_answer") {
			parentForm = jqueryObj.closest('form');			
			jqueryObj.parent().remove();
			parentForm.find('.add_answer:last').show();
		}
	}

});


