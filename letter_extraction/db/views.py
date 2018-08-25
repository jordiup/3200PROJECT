from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response

from .models import *
from .models import metadata_extraction
import logging

# Create your views here.

from django.template import RequestContext

logger = logging.getLogger(__name__)

def index(request):
    context = {}
    return render(request, 'db/index.html', context)


def search(request):
    template = loader.get_template('db/metadata.html')
    metadata_categories = metadata_extraction()
    context = {
    }
   # return HttpResponse(template.render(context, request), {'container' : ['adawdadawd']})
    return render(request, 'db/metadata.html' , {"metadata_categories" : metadata_categories})

def search_result(request):
    context = {}
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
