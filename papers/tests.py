#from django.core.urlresolvers import reverse
from django.utils import timezone
from django.test import TestCase, Client

from papers.models import Sender, Paper, Question, Answer
from papers.views import sanitizeInput, getAnswers, checkExistingEmail,email_has_more_than_five_questions_open

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
		#Empty string
		self.assertEqual(sanitizeInput("", "email"), False)
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
		self.assertEqual(sanitizeInput("Thingster@gmail.com", "email"), "thingster@gmail.com")

	def test_sanitize_input_question_type_incorrect_type_with_incorrect_strings(self):
		'''
		This should return false unless the string is Open | Secret | Multiple
		'''
		#Open in the string but words after
		self.assertEqual( sanitizeInput("Open Deck", "question_type"), False )		
		#Secret in the string but words after
		self.assertEqual( sanitizeInput("Secrets", "question_type"), False )		
		#Multiple in the string but words after
		self.assertEqual( sanitizeInput("Multiple Love", "question_type"), False )		
		#Empty string
		self.assertEqual( sanitizeInput("", "question_type"), False )		

	def test_sanitize_input_question_type_correct_types(self):
		'''
		This should return false unless the string is Open | Secret | Multiple
		When true it should return the string passed (ex: Open/Secret/Multiple)
		'''		
		self.assertEqual(sanitizeInput("Multiple", "question_type"), "Multiple")
		#Secret in the string but words after
		self.assertEqual(sanitizeInput("Secret", "question_type"), "Secret")
		#Multiple in the string but words after
		self.assertEqual(sanitizeInput("Open", "question_type"), "Open")

	#Placeholder for sanitize input question
	#Placeholder for sanitize input selected_answer

	def test_get_answers_with_10_answers(self):
		'''
		Method should be passed raw post_data and return a list of answers gleaned from the dictionary.
		Any key with 'answertext' whose length is greater than 0 should have its value taken and inserted 
		into the returned list along with the number after answertext-.  
		This test passes the method 10 answers and expects them all back in a list.
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
		self.assertEqual(sorted(getAnswers(testDictionary)), sorted([
																	['Answer1', 1], 
																	['Answer2', 2],
																	['Answer3', 3],
																	['Answer4', 4],
																	['Answer5', 5],
																	['Answer6', 6], 
																	['Answer7', 7],
																	['Answer8', 8],
																	['Answer9', 9],
																	['Answer10', 10]
																	]) )

	def test_get_answers_with_1_answer(self):
		'''
		When passed a dictionary that has less than 2 answers, the method should return False
		'''
		testDictionary = {
		'answertext-1': "Answer1"
		}

		self.assertEqual(getAnswers(testDictionary), False)

	def test_check_existing_email_query_without_email(self):
		'''
		A Django DB APi query is performed to check for an existing e-mail and if it exists in the DB,
		Will return its primary key. Otherwise a fresh DB instance object will be returned. 
		'''		
		test_email = checkExistingEmail('calcal@gmail.com')
		self.assertEqual(test_email.email , 'calcal@gmail.com' )

	def test_check_existing_email_query_with_existing_email(self):
		'''
		A Django DB APi query is performed to check for an existing e-mail and if it exists in the DB,
		Will return its primary key. Otherwise a fresh DB instance object will be returned. 
		'''		
		new_email1 = Sender(email="calcutta@gmail.com", ip="10.10.10.11")		
		new_email2 = Sender(email="calcal@gmail.com", ip="10.10.10.10")	
		new_email1.save()
		new_email2.save()		

		test_email = checkExistingEmail('calcal@gmail.com')

		self.assertEqual(test_email.email, 'calcal@gmail.com' )
		self.assertEqual(test_email.ip, '10.10.10.10')

	def test_email_has_more_than_five_questions_with_five_questions(self):
		'''
		Method will return true if 5 or more papers exist for a certain e-mail.
		E-Mail is passed as a string for a count query. Creating 5 papers.
		'''
		sent_from = Sender(email="calcal@gmail.com", ip="10.10.50.50")
		sent_from.save()
		for x in range(5):
			paper = Paper(sender=sent_from, sent_to="bobbie@gmail.com", active_until=timezone.now())
			paper.save()		
		self.assertEqual(email_has_more_than_five_questions_open('bobbie@gmail.com'), True)

	def test_email_has_more_than_five_questions_with_three_questions(self):
		'''
		Method will return true if 5 or more papers exist for a certain e-mail.
		E-Mail is passed as a string for a count query. Creating 3 papers.
		'''
		sent_from = Sender(email="calcal@gmail.com", ip="10.10.50.50")
		sent_from.save()
		for x in range(3):
			paper = Paper(sender=sent_from, sent_to="bobbie@gmail.com", active_until=timezone.now())
			paper.save()		
		self.assertEqual(email_has_more_than_five_questions_open('bobbie@gmail.com'), False)

	def test_email_has_more_than_five_questions_with_zero_questions(self):
		'''
		Method will return true if 5 or more papers exist for a certain e-mail.
		E-Mail is passed as a string for a count query. Creating 0 papers.
		'''
		self.assertEqual(email_has_more_than_five_questions_open('bobbie@gmail.com'), False)




	'''Example web page testing with POST (from official docs)
		def web_page_test(self):
			c = Client() #instantiate faux web Client
			response = c.post('papers/ask.html', {'question': 'Who do you like?', 'Answertext-1: "Me?" })			
			self.assertEqual(response.status_code, 200)

			response.get('papers/index.html') #May not have the url syntax right
			#https://docs.djangoproject.com/en/1.6/topics/testing/tools/

	'''

	#Placeholder for get_client_ip() tests
	#Placeholder for create_new_pape
	#Placeholder for create_answers_objects	
	#Placeholder for 