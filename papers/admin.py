from django.contrib import admin
from papers.models import Sender, Paper, Question, Answer

#Tabular Classes
class QuestionInLine(admin.TabularInline):	
	model = Question
	can_delete = False
	extra = 0
	fields = (('question_text'),)	
	readonly_fields = ('question_text',)

class AnswerInLine(admin.StackedInline):
	#Only show the answer the requester selected
	def get_queryset(self, request):
		querySet = super(AnswerInLine, self).get_queryset(request)
		return querySet.filter(isSelected=True)

	def get_the_code(self, instance):
		return (instance.get_code())

	def get_sent_to(self, instance):
		return (instance.get_sent_to())

	#Prevent adding answers from the form
	def get_max_num(self, request, obj=None, **kwargs):		
		return 0

	can_delete = False
	model = Answer
	readonly_fields = ('get_sent_to', 'question', 'get_the_code', 'paper')
	fields = ('get_sent_to', 'question', 'get_the_code', 'paper')	

	get_the_code.short_description = "Access Code"
	get_sent_to.short_description = "Sent To"


class PaperInLine(admin.StackedInline):
	#Prevent adding papers from the form
	def get_max_num(self, request, obj=None, **kwargs):		
		return 0
	model = Paper
	readonly_fields = ('active_until',)	
	fields = ('active_until',)
	extra = 0




#Admin pages
class SenderAdmin(admin.ModelAdmin):	
	readonly_fields = ('email', 'ip',)

	fieldsets = [
		( "Sender Information",	{'fields': (('email', 'ip'),)} ),
	]

	inlines = [			
		AnswerInLine,
		PaperInLine,
	]

class PaperAdmin(admin.ModelAdmin):
	list_display = ('sender', 'sent_to', 'active_until')
	list_filter = ('active_until',)	
	search_fields = ('sent_to',)	
	ordering = ('sender','active_until')	
	inlines = [QuestionInLine]


admin.site.register(Sender, SenderAdmin)
#admin.site.register(Paper, PaperAdmin)