from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.forms import ModelForm

from papers.models import Sender, Paper, Question, Answer

WEBSITE_NAME = "Doubleblind"

class QuestionForm(ModelForm):
	class Meta:
		model = Question
		fields = ('sender', 'paper', 'question_type', 'question_text')

def getAnswers(post_data):
	answers = []
	for question_info in post_data:
		if 'answertext' in question_info:
			answer_text = post_data[question_info]
			if len(answer_text) > 0:
				answers.append(str(answer_text))

	return (answers)	
	
def sanitizeInput(string_input, sanitize_type="generic"):
	if sanitize_type == "generic":
		return (string_input.replace("<", "") )
	elif sanitize_type == "email":
		#Strip out extra + email filters				

		if "+" in string_input:
			at_location = string_input.find("@")	
			plus_location = string_input.find("+")									
			sliced_domain = string_input[at_location:len(string_input)]
			sliced_email = string_input[:plus_location]
			string_input = sliced_email + sliced_domain
		#Remove extra periods
		if "@gmail.com" in string_input:
			at_location = string_input.find("@")
			sliced_email = string_input[:at_location]
			sliced_domain = string_input[at_location:len(string_input)]			
			sliced_email = sliced_email.replace(".", "")
			string_input = sliced_email + sliced_domain

		return string_input

# Create your views here.
def Index(request):
	template_name = 'papers/index.html'
	latest_senders = Sender.objects.all()

	return render(request, template_name, {'latest_senders': latest_senders,
												'site_name': WEBSITE_NAME,} )

def Ask(request):
	template_names = 'papers/ask.html'		
	return render(request, template_names, {'site_name': WEBSITE_NAME,} )

def queueQuestion(request):			
	try:
		#All POST data is apparently sanitized by django		
		post_data = request.POST
		#question_text = post_data['question_text']
		sender = post_data['sender']
		sent_to = sanitizeInput(post_data['sent_to'], 'email')
		answers = getAnswers(post_data)
		
		print post_data		
		




	except Exception:
		for error in Exception:
			print(str(error))	

	return (HttpResponseRedirect('/ask') )
