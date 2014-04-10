from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

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

	return render(request, template_names, {'site_name': WEBSITE_NAME})