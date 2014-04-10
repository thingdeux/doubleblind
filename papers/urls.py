from django.conf.urls import patterns, include, url

from papers import views

urlpatterns = patterns('',	
	#index page /
	url(r'^ask/$', views.Ask, name='ask'),
	url(r'^$', views.Index, name='index'),	
)