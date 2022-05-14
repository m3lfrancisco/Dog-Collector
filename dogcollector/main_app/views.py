from django.shortcuts import render
from django.http import HttpResponse
from . models import *

# Create your views here.
def home(request):
    """
    home view
    http://localhost:8000/
    """
    return HttpResponse('<h1>Hello</h1>')

def about(request):
    """
    about view
    http://localhost:8000/about/
    """
    return render(request, 'about.html')

def dogs_index(request):
    return render(request, 'dogs/index.html', {'dogs': dogs_list})