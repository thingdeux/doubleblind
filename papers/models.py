from datetime import datetime, timedelta
from django.db import models
import uuid

def get_tomorrows_date():
		return ( datetime.now() + timedelta(days=1) )

def get_random_uuid():
	return (uuid.uuid4())

class Sender(models.Model):
	email = models.EmailField(max_length=254, unique=True)
	ip = models.IPAddressField()

	def __unicode__(self):
		return(self.email)

class Paper(models.Model):
	sender = models.ForeignKey(Sender)
	sent_to = models.EmailField(max_length=254)
	code = models.CharField(max_length=32, default=get_random_uuid())
	#The default time for a paper to be active is 1 day
	active_until = models.DateField(auto_now=False, default=get_tomorrows_date(), db_index=True )
	allow_requests_sent_from = models.BooleanField(default=False)	

	def __unicode__(self):
		return(self.id)

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
		return(self.question_text)

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

	def get_code(self):
		return (self.paper.code)

	def get_sent_to(self):
		return (self.paper.sent_to)

	def __unicode__(self):
		return(self.answer_text)