import datetime
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from .forms import *
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from db.services import query_service, account_service, upload_service, store_service,  results_service, model_service
from .models import *

#Testing import python function

# Create your views here.

from django.template import RequestContext

result = {}
indicator = 0
archive_number_list = []
previous_url = ""

@login_required
def index(request):
    context = {'myflag':'False'}
    if request.method == "POST":
        global result
        global indicator
        global archive_number_list
        store_service.deleteReplicates(archive_number_list)
        if indicator == 0:
            try:
                store_service.addToModel(result, request.user)
                context = {'myflag':'True'}
            except:
                errmsg = 'Storing of letters were not successful! Contact administrator for further details!'
                return render(request,'db/upload.html',{'err': errmsg, 'errtype': 'store'})
        elif indicator == 1:
            try:
                store_service.addToModel_xlsx(result, request.user)
                context = {'myflag':'True'}
            except:
                errmsg = 'Storing of letters were not successful! Contact administrator for further details!'
                indicator = 0
                return render(request,'db/upload.html',{'err': errmsg, 'errtype': 'store'})
            indicator = 0
    result = {}
    archive_number_list = []
    return render(request, 'db/index.html', context)


@login_required
def search(request):
    if not request.user.has_perm('db.can_search'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    template = loader.get_template('db/search.html')
    header = ['Archive Number', 'Date Written', 'Document Type', 'Language', 'Place Written', 'Sender Name', 'Place Received', 'Receiver Name']
    values = query_service.analyze_query_request("", "", True)
    context = {'header': header, 'values':values}
    return HttpResponse(template.render(context, request))

    # search by archive numbers, use that to get some document
    # docs.obj.filter - you can find on djjango doc
    # should be a list of documents
    # feed it into return_doc ([], the doc shit)


@login_required
def search_result(request):
    global previous_url
    previous_url = ""
    if not request.user.has_perm('db.can_search'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    search_type = str(request.GET['searchtype'])
    query_value = str(request.GET['query'])
    values = query_service.analyze_query_request(search_type, query_value, False)
    header = ['Archive Number', 'Date Written', 'Document Type', 'Language', 'Place Written', 'Sender Name', 'Place Received', 'Receiver Name', 'Edit']
    #primary_keys = query_service.get_pks(values)
    context = {'header': header, 'values': values}
    return render(request, 'db/result.html', context)


@login_required
def upload(request):
    if not request.user.has_perm('db.can_upload'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    if request.method == "POST" and  request.FILES.get('myfile',False):
        if ((not request.FILES['myfile'].name.endswith('.xlsx')) and (not request.FILES['myfile'].name.endswith('.xls')) and (not request.FILES['myfile'].name.endswith('.docx'))):
            return render(request,'db/upload.html',{"fname":request.FILES['myfile'].name , 'errtype': 'preview'})
        global indicator
        global result
        global archive_number_list
        result, errmsg = upload_service.main(request.FILES['myfile'])
        results_service.archive_number_finder(result, archive_number_list) #checking for duplicates, duplicate archive numbers will be stored in archive_number_list
        indicator = 0 #docx files
        if (request.FILES['myfile'].name.endswith('.xlsx') or request.FILES['myfile'].name.endswith('.xls')):
            indicator = 1 #xlsx and xls files
        return render(request,'db/upload.html',{"list":result, "indic": indicator, "fname": request.FILES['myfile'].name, 'err': errmsg, 'errtype': 'preview'})
    else:
        template = loader.get_template('db/upload.html')
        context = {}
    return render(request,'db/upload.html',context)

@login_required
def edit(request, items):
    if not request.user.has_perm('db.can_edit'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    forms = get_forms_by_document(request, items)
    context = {}
    if request.method == "POST":
        if forms[0].is_valid():
            instance = forms[0].save(commit=False)
            instance.save()
            context["update_message"] = 'Successfully updated!'
            return render(request, 'db/edit.html', context)
        else:
            context["update_message"] = 'Update failed!'
            return render(request, 'db/edit.html', context)   
    context = {
        'document_form' : forms[1],
        'sender_form' : forms[2],
        'receiver_form' : forms[3],
        'sender_location_form' : forms[4],
        'receiver_location_form' : forms[5],
        }
    return render(request, 'db/edit.html', context)


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

def drag_n_drop_test(request):
    context = {}
    return render(request, 'db/drag_n_drop_test.html', context)

@login_required
def labels(request):
    if not request.user.has_perm('db.can_edit'):
        return render(request, 'db/index.html', {"message":"You do not have the permissions to perform this task!"})
    if 'new_label' in request.GET:
        model_service.add_metadata_label(request.GET['new_label'])
    labels = model_service.get_metadata_labels()
    context = {'labels':labels}
    return render(request, 'db/labels.html', context)
