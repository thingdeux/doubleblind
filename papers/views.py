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
	def getAnswers(post_data):
			answers = []
			for question_info in new_question:
				if 'answertext' in question_info:
					answer_text = post_data[question_info]
					if len(answer_text) > 0:
						answers.append(str(answer_text))

			return (answers)	

	def combineAndParseDataFromPOST(post_data):
		question_text = post_data['question_text']
		sender = post_data['sender']
		sent_to = post_data['sent_to']
		answers = getAnswers(post_data)
	
	try:
		#All POST data is apparently sanitized by django
		new_question = request.POST
		postedData = combineAndParseDataFromPOST(new_question)

		print dataDict




	except Exception:
		for error in Exception:
			print(str(error))	

	return (HttpResponseRedirect('/ask') )
