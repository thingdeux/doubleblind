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
	try:
		new_question = request.POST
		for thing in new_question:
			print (str(thing))
	except Exception:
		for error in Exception:
			print(str(error))


	return (HttpResponseRedirect('/ask') )
