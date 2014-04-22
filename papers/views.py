from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.forms import ModelForm
import re

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

	if len(answers) >= 2:
		return (answers)	
	else:
		return False
	
def sanitizeInput(string_input, sanitize_type="generic"):
	if len(string_input) > 5:
		if sanitize_type == "generic":
			return (string_input.replace("<", "") )
		elif sanitize_type == "question":
			if len(string_input) < 512:
				return string_input.lower()
		elif sanitize_type == "email":
			#Check to see if the passed string 'looks like' an email address
			if not re.match(r"[^@]+@[^@]+\.[^@]+", string_input):
				return False

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

			return string_input.lower()
	else:
		return False

def checkExistingEmail(email_to_query):
	existing = Sender.objects.filter(email=email_to_query)	
	if len(existing) > 0:		
		return ( existing[0] )
	else:
		return ( Sender(email=email_to_query) )

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def email_has_more_than_five_questions_open(email_to_query):
	the_count = Paper.objects.filter(sent_to=email_to_query).count()	
	if the_count >= 5:
		return True
	else:
		return False


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
		question_text = sanitizeInput(post_data['question_text'], 'question')
		sender = sanitizeInput(post_data['sender'], 'email').lower()		
		answers = getAnswers(post_data)
		#An empty sent_to will generate a custom url for use
		if len(post_data['sent_to']) >= 1:
			sent_to = sanitizeInput(post_data['sent_to'], 'email').lower()
		else:
			sent_to = "Generate"
		
		if (sender is not False and sent_to is not False and 
			answers is not False and question_text is not False):
			#Input has been sanitized and checked and can be inserted into the DB
			the_sender = checkExistingEmail(sender)
			the_sender.ip = get_client_ip(request)

			if email_has_more_than_five_questions_open(sent_to):
				print ("Sorry bud")
			else:
				print ("You're ok!")
				#Verify no more than 5 questions are open to a single e-mail
				#paper = (sender=the_sender, sent_to=)
			
		else:			
			#Throw an error, something is incorrect
			incorrectFields = []
			if sender == False:
				incorrectFields.append("Your E-mail")
			if sent_to == False:
				incorrectFields.append("Recipients E-mail")
			if question_text == False:
				incorrectFields.append("Question")
			if answers == False:
				incorrectFields.append("Answers")


			response = HttpResponse()
			response.status_code = 400

			response.reason_phrase = "Error in field(s): " + ' | '.join(incorrectFields)
			return response
		




	except Exception:		
		return (HttpResponseRedirect('/ask') )
