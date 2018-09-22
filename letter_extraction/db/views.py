import datetime
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from db.services import query_service, account_service, upload_service, store_service
from .models import *

#Testing import python function

# Create your views here.

from django.template import RequestContext

result = {}

@login_required
def index(request):
    if request.method == "POST":
        global result
        store_service.addToModel(result)
        result = {}
    context = {}
    return render(request, 'db/index.html', context)


@login_required
def search(request):
    if not request.user.has_perm('db.can_search'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    template = loader.get_template('db/search.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


@login_required
def search_result(request):
    if not request.user.has_perm('db.can_search'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    search_type = str(request.GET['searchtype'])
    query_value = str(request.GET['query'])
    document_list = query_service.analyze_query_request(search_type, query_value)
    # categories = {}
    # metadata = {}
    # storeFunction.string_split(document_list, categories, metadata)
    # print(categories)
    # print(metadata)
    context = {'document_list': document_list}
    return render(request, 'db/result.html', context)


@login_required
def upload(request):
    if not request.user.has_perm('db.can_upload'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    if request.method == "POST" and  request.FILES.get('myfile',False):
        print("sad")
        global result
        result = upload_service.main(request.FILES['myfile'])
        indicator = 0 #docx files
        if (request.FILES['myfile'].name.endswith('.xlsx') or request.FILES['myfile'].name.endswith('.xls')):
            indicator = 1 #xlsx and xls files
        #storing(result)
        return render(request,'db/upload.html',{"list":result, "indic": indicator})
    else:
        template = loader.get_template('db/upload.html')
        context = {}
    return render(request,'db/upload.html',context)


def login_user(request):
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
