from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render_to_response
from django.conf import settings # added by @jordi
from django.core.files.storage import FileSystemStorage # added by @jordi

from .models import *

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


def login(request): # added by @jordi
    template = loader.get_template('db/login.html')
    context = {
    }
    return HttpResponse(template.render(context, request))

def simple_upload(request): # added by @jordi
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'core/simple_upload.html', {
            'uploaded_file_url': uploaded_file_url
        })
    return render(request, 'core/simple_upload.html')
