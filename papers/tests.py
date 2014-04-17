#from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from papers.models import Sender, Paper, Question, Answer
from papers.views import sanitizeInput

# Create your tests here.
class AskViewTests(TestCase):
	def test_sanitize_input_plus_signs_included(self):
		'''
		An e-mail with + signs in it should be stripped of everything after the +
		with the exception of the @address.com
		'''		
		self.assertEqual(sanitizeInput("thingster+extra+stuff-1213@yahoo.com", "email"), "thingster@yahoo.com")


	def test_sanitize_input_extra_periods_with_gmail_email_address(self):
		'''
		A gmail e-mail with . characters before the @address.com should be stripped of all periods.
		'''
		self.assertEqual(sanitizeInput("th.i.n..gst.er@gmail.com", "email"), "thingster@gmail.com")

	def test_sanitize_input_extra_periods_without_gmail_email_address(self):
		'''
		A gmail e-mail with . characters before the @address.com should be stripped of all periods.
		'''
		self.assertEqual(sanitizeInput("th.i.n..gst.er@yahoo.com", "email"), "th.i.n..gst.er@yahoo.com")