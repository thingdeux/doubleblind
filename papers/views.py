from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.forms import ModelForm
import re

from papers.models import Sender, Paper, Question, Answer

WEBSITE_NAME = "Doubleblind"

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
		#All POST data is apparently escaped by Django
		#Sanitizing and checking additional criteria		
		post_data = request.POST
		question_text = sanitizeInput(post_data['question_text'], 'question')
		sender = sanitizeInput(post_data['sender'], 'email').lower()		
		question_type = sanitizeInput( post_data['question_type'], 'question_type')

		#An empty 'sent'_to will generate a custom url for use
		if len(post_data['sent_to']) >= 6:
			sent_to = sanitizeInput(post_data['sent_to'], 'email').lower()
		else:
			sent_to = "Generate"	

		if question_type == "Multiple" or question_type == "Secret":
			answers = getAnswers(post_data)						
			
			#Typecast the answer radio button value to verify it's a normal number
			try:
				selected_answer = int( post_data['selected_answer'] )
			except:
				selected_answer = False
		else:
			selected_answer = "Open"
			answers = "Open"		
		
		if (sender is not False and sent_to is not False and 
			answers is not False and question_text is not False and
			selected_answer is not False and question_type is not False):
			#Input has been sanitized and checked and can be inserted into the DB			
			create_new_paper(sender=sender, ip=get_client_ip(request), question=question_text,
							 sent_to=sent_to, answers=answers, selected_answer=selected_answer,
							 question_type=question_type)
			
		else:			
			#Build and throw an error, some input is incorrect
			#This should be caught with Javascript but including checks on back-end as well.
			#Can't trust users
			incorrectFields = []
			if sender == False:
				incorrectFields.append("Your E-mail")
			if sent_to == False:
				incorrectFields.append("Recipients E-mail")
			if question_text == False:
				incorrectFields.append("Question")
			if answers == False:
				incorrectFields.append("Answers")

			#Return http response with error code 400 and text with incorrect fields.
			response = HttpResponse()
			response.status_code = 400

			response.reason_phrase = "Error in field(s): " + ' | '.join(incorrectFields)
			return response
	

	except Exception:		
		return (HttpResponseRedirect('/ask') )


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
				answers.append( [str(answer_text), int(question_info[11:]) ] )

	if len(answers) >= 2:
		return (answers)	
	else:
		return False

def sanitizeInput(string_input, sanitize_type="generic"):	
	#Various options for sanitizing different user input
	if len(string_input) >= 4:
		if sanitize_type == "generic":
			return (string_input.replace("<", "") )
		elif sanitize_type == "question":
			if len(string_input) <= 512:
				return string_input.lower()				
		elif sanitize_type == "question_type":
			if string_input in ['Open', 'Multiple', 'Secret']:				
				return string_input
			else:
				return False		
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
	#Acquire clients IP from http headers
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def email_has_more_than_five_questions_open(email_to_query):
	#Verify no more than 5 questions are open to a single e-mail
	the_count = Paper.objects.filter(sent_to=email_to_query).count()	
	if the_count >= 5:
		return True
	else:
		return False

def create_new_paper(**kwargs):	
	if email_has_more_than_five_questions_open(kwargs['sent_to']):
		#Do not create a new paper and return http response with error code 400		
		response = HttpResponse()
		response.status_code = 400
		response.reason_phrase = "Too many questions open for this e-mail"
		return response
	else:	#Insert Data into DB		
		#See if a DB record from the sender already exists.
		the_sender = checkExistingEmail(kwargs['sender'])			
		the_sender.ip = kwargs['ip']		
		the_sender.save()

		new_paper = Paper(sender=the_sender, sent_to=kwargs['sent_to'])
		new_paper.save()
		new_question = Question(sender=the_sender, paper=new_paper, question_text=kwargs['question'],
								question_type=kwargs['question_type'])		
		new_question.save()
		new_answers = create_answers_objects(the_sender, new_paper, new_question, 
											kwargs['answers'], kwargs['selected_answer'])		
				
		test = Answer.objects.bulk_create(new_answers)
		test.save()

							
def create_answers_objects(sender, paper, question, answers, selected_answer):
	#Create django answer objects from a list of answers	
	if question.question_type == "Multiple" or question.question_type == "Secret":		
		answers_to_return = []		
		for an_answer in answers:
			new_answer = Answer(sender=sender, paper=paper, question=question)		
			new_answer.answer_text = an_answer[0]		
			if an_answer[1] == selected_answer:
				new_answer.isSelected = True								
			
			answers_to_return.append(new_answer)

		return answers_to_return
	else:
		answers_to_return = []
		new_answer = Answer(sender=sender, paper=paper, question=question)
		new_answer.answer_text = "Open"	
		return answers_to_return