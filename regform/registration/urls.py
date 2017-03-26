from django.conf.urls import url, include
from django.views.generic import ListView, DetailView
from django.contrib.auth import views as auth_views
from . import views as useradmin_views

urlpatterns = [ 
				url(r'^register/$', useradmin_views.register),
				url(r'^text/$', useradmin_views.textappend),
				url(r'^register/success/$', useradmin_views.register_success),
            ]
