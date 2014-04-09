from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import timezone

from papers.models import Sender, Paper, Question, Answer

WEBSITE_NAME = "Doubleblind"

# Create your views here.
def IndexView(request):
	template_name = 'papers/index.html'
	latest_senders = Sender.objects.all()

	return render(request, 'papers/index.html', {'latest_senders': latest_senders,
												'site_name': WEBSITE_NAME,} )