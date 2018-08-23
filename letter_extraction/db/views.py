from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.shortcuts import render_to_response
#from .models import *

# Create your views here.

from django.template import RequestContext

def index(request):
    
    context = {}
    return render(request, 'db/index.html', context)


def search(request):
    template = loader.get_template('db/search.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def search_result(request):
    template = loader.get_template('db/result.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def upload(request):
    template = loader.get_template('db/upload.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('db/login.html')
    if request.method=="POST":
        print("they tried to log in!!!")
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            print('good boi')
            #log in user
            return HttpResponseRedirect('db:index')
        else:
            # TODO: should refresh login page, currently goes to index
            print('evil')
            return redirect('db:index')
    context = {'form':AuthenticationForm()}
    return HttpResponse(template.render(context, request))