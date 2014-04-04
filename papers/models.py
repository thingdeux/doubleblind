from datetime import datetime, timedelta
from django.db import models

def get_tomorrows_date():
		return ( datetime.now() + timedelta(days=1) )

class Sender(models.Model):
	email = models.EmailField(max_length=254)
	ip = models.IPAddressField()

	def __unicode__(self):
		return(self.email)

class Paper(models.Model):	
	sender = models.ForeignKey(Sender)
	sent_to = models.EmailField(max_length=254)
	#The default time for a paper to be active is 1 day
	active_until = models.DateField(auto_now=False, default=get_tomorrows_date(), db_index=True )
	allow_requests_sent_from = models.BooleanField(default=False)	

	def __unicode__(self):
		return(self.sent_to)

class Question(models.Model):
	sender = models.ForeignKey(Sender)
	#Each paper can only have one question
	paper = models.OneToOneField(Paper, primary_key=True)

	QUESTION_TYPES = (
		('Multiple', 'Multiple Choice'),
		('Open', 'Open-Ended'),
		('Secret', 'Secret Response'),
	)

	question_type = models.CharField(max_length=8, choices=QUESTION_TYPES, default="Multiple")
	question_text = models.CharField(max_length=512)

	def __unicode__(self):
		return(self.question_type)

class Answer(models.Model):
	sender = models.ForeignKey(Sender)
	paper = models.ForeignKey(Paper)	
	question = models.ForeignKey(Question)


	answer_text = models.CharField(max_length=512)
	isSelected = models.BooleanField(default=False)
	secret_text = models.CharField(max_length=512, blank=True)
	secret_response = models.CharField(max_length=512, blank=True)
	secret_guesses = models.IntegerField(default=1, blank=True)
	open_ended_response = models.CharField(max_length=512, blank=True)

	def __unicode__(self):
		return(self.answer_text)