from django.contrib import admin
from papers.models import Sender, Paper, Question, Answer

# Register your models here.
class QuestionInLine(admin.TabularInline):
	model = Question	
	extra = 0	
	#fields = (('question_type', 'question_text'),)
	radio_fields = {"paper": admin.VERTICAL}

class AnswerInLine(admin.TabularInline):	
	model = Answer
	'''
	fields = (('isSelected','answer_text', 'secret_text', 
		'secret_response', 'secret_guesses', 'open_ended_response'))'''
	extra = 0

class PaperInLine(admin.StackedInline):
	model = Paper	
	extra = 0

class SenderAdmin(admin.ModelAdmin):	
	fieldsets = [
		( None,	{'fields': ['email', 'ip']} ),		
	]

	inlines = [
		PaperInLine,
		QuestionInLine,
		AnswerInLine,
	]

class PaperAdmin(admin.ModelAdmin):
	list_display = ('sender', 'sent_to', 'active_until')
	list_filter = ('active_until',)
	search_fields = ('sent_to',)	
	ordering = ('sender','active_until')	
	inlines = [QuestionInLine]


admin.site.register(Sender, SenderAdmin)
admin.site.register(Paper, PaperAdmin)