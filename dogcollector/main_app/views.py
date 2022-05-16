from django.shortcuts import render
from django.http import HttpResponse
from .models import Dog

import logging
logging.basicConfig(level=logging.DEBUG)


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
    """
    dogs index page
    http://localhost:8000/dogs/
    """
    logging.info('calling dogs_index')
    dogs = Dog.objects.all()
    return render(request, 'dogs/index.html', {'dogs': dogs})

def dogs_detail(request, dog_id):
    """
    dog detail page
    http://localhost:8000/dogs/1/
    """
    logging.info('calling dog_detail')
    dog = Dog.objects.get(id=dog_id)
    return render(request, 'dogs/detail.html', {'dog': dog})