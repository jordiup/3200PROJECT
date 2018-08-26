from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render

from db.services import query_service

from django.shortcuts import render_to_response
from django.db.models import Q

from .models import *
import datetime

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
    template = loader.get_template('db/upload.html')
    context = {
    }
    return HttpResponse(template.render(context, request))


def login(request):
    template = loader.get_template('db/login.html')
    context = {
    }
    return HttpResponse(template.render(context, request))