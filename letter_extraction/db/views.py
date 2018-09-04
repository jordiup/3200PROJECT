import datetime
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from db.services import query_service, account_service, upload_service
from .models import *

#Testing import python function

# Create your views here.

from django.template import RequestContext


@login_required
def index(request):
    context = {}
    return render(request, 'db/index.html', context)


@login_required
def search(request):
    template = loader.get_template('db/search.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


@login_required
def search_result(request):
    search_type = str(request.GET['searchtype'])
    query_value = str(request.GET['query'])
    document_list = query_service.analyze_query_request(search_type, query_value)
    context = {'document_list': document_list}
    return render(request, 'db/result.html', context)

def storing(myletters):
    for each in myletters:
        for data in each:
            print(data)

@login_required
def upload(request):
    if request.method == 'POST' and request.FILES.get('myfile',False):
        result = upload_service.main(request.FILES['myfile'])
        indicator = 0 #docx files
        if (request.FILES['myfile'].name.endswith('.xlsx')):
            indicator = 1 #xlsx files
        #storing(result)
        return render(request,'db/upload.html',{"list":result, "indic": indicator})
    else:
        template = loader.get_template('db/upload.html')
        context = {}
    return render(request,'db/upload.html',context)

def login(request):
    message = None
    if request.method=="POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            if account_service.login_user(request):
                return redirect('db:index')
        else:
            context = {'form':AuthenticationForm(), 'message':'Username or password incorrect!'}
    else:
        context =  {'form':AuthenticationForm(), 'message':message}
    return render(request, 'db/login.html', context)


def logout(request):
    account_service.logout_user(request)
    return redirect('db:login')