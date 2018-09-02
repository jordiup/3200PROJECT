from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from db.services import query_service

from django.shortcuts import render_to_response
from django.db.models import Q

from .models import *
import datetime

#Testing import python function
import db.myscan as processletter

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
    search_type = str(request.GET['searchtype'])
    query_value = str(request.GET['query'])
    document_list = query_service.analyze_query_request(search_type, query_value)
    context = {'document_list': document_list}
    return render(request, 'db/result.html', context)


def upload(request):
    if request.method == 'POST' and request.FILES.get('myfile',False):
        result = processletter.main(request.FILES['myfile'])
        indicator = 0 #docx files
        if (request.FILES['myfile'].name.endswith('.xlsx')):
            indicator = 1 #xlsx files
        return render(request,'db/upload.html',{"list":result, "indic": indicator})
    else:
        template = loader.get_template('db/upload.html')
        context = {}
    return render(request,'db/upload.html',context)


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
