#from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase

from papers.models import Sender, Paper, Question, Answer
from papers.views import sanitizeInput, getAnswers

# Create your tests here.
class AskViewMethodTests(TestCase):
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
		A non gmail e-mail with . characters before the @address.com should not be stripped of all periods.
		'''
		self.assertEqual(sanitizeInput("th.i.n..gst.er@yahoo.com", "email"), "th.i.n..gst.er@yahoo.com")

	def test_sanitize_input_empty_email(self):
		'''
		If sanitizeInput receives a string that doesn't "look" like an e-mail, should return false.
		'''
		self.assertEqual(sanitizeInput("", "email"), False)

	def test_sanitize_input_not_a_proper_email(self):
		'''
		If something not matching an e-mail is passed to the sanitizeInput method it should return False.
		'''
		#Just text with no @ ... '.com'
		self.assertEqual(sanitizeInput("CherryPy", "email"), False)
		#Just text and a .com with no @
		self.assertEqual(sanitizeInput("towermunchkin.com", "email"), False)
		#Just an @ with no .com
		self.assertEqual(sanitizeInput("CherryPy@", "email"), False)
		#An @ and a .com right next to each other with no domain
		self.assertEqual(sanitizeInput("CherryPy@.com", "email"), False)

	def test_sanitize_input_proper_email(self):
		'''
		If something not matching an e-mail is passed to the sanitizeInput method it should return False.
		'''
		self.assertEqual(sanitizeInput("thingster@gmail.com", "email"), "thingster@gmail.com")

	def test_get_answers_with_10_answers(self):
		'''
		Method should be passed raw post_data and return a list of answers gleaned from the dictionary.
		Any key with 'answertext' whose length is greater than 0 should have its value taken and inserted 
		into the returned list.  This test passes the method 10 answers and expects them all back in a list.
		'''
		testDictionary = {
			'answertext-1': "Answer1",
			'answertext-2': "Answer2",
			'answertext-3': "Answer3",
			'answertext-4': "Answer4",
			'answertext-5': "Answer5",
			'answertext-6': "Answer6",
			'answertext-7': "Answer7",
			'answertext-8': "Answer8",
			'answertext-9': "Answer9",
			'answertext-10': "Answer10",
		}
		#Sorting for list comparison purposes
		self.assertEqual(sorted(getAnswers(testDictionary)), sorted(['Answer1', 'Answer2', 'Answer3', 'Answer4', 'Answer5',
																	'Answer6', 'Answer7', 'Answer8', 'Answer9', 'Answer10']) )

	def test_get_answers_with_1_answer(self):
		'''
		When passed a dictionary that has less than 2 answers, the method should return False
		'''
		testDictionary = {
		'answertext-1': "Answer1"
		}

		self.assertEqual(getAnswers(testDictionary), False)

