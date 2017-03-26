from django.shortcuts import render
from django.http import *
from django.shortcuts import render_to_response,redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.db.models import Q
from django.views.decorators.csrf import ensure_csrf_cookie
import re
from django.views.decorators.csrf import csrf_exempt


from registration.forms import RegistrationForm, TextForm

def index(request):
    return render(request, 'registration/header.html')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['firstname'],
            last_name=form.cleaned_data['lastname'],
            is_active=False,
            )
            return HttpResponseRedirect('success/')
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/register.html',
    variables,
    )


@csrf_exempt
def textappend(request):
    if request.method == 'POST':
        form = TextForm(request.POST)
        if form.is_valid():
            text=form.cleaned_data['text']
            filename=form.cleaned_data['filename']
            with open(filename, "a") as myfile:
                myfile.write(text)
            return HttpResponseRedirect('/text')
    else:
        form = TextForm()
    variables = RequestContext(request, {
    'form': form
    })
 
    return render_to_response(
    'registration/text.html',
    variables,
    )

  
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )
