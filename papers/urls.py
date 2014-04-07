from django.conf.urls import patterns, include, url

from papers import views

urlpatterns = patterns('',
	#index page /
	url(r'^$', views.IndexView, name='index'),
)