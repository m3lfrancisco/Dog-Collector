import os
import boto3
import uuid
from django.shortcuts import render, redirect 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.urls import reverse
from .models import Dog, Toy, Photo
from .forms import FeedingForm

import logging
logging.basicConfig(level=logging.DEBUG)

# Create your views here.
def home(request):
    """
    home view
    http://localhost:8000/
    """
    return render(request, 'home.html')

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
    toys_dog_doesnt_have = Toy.objects.exclude(id__in = dog.toys.all().values_list('id'))
    return render(request, 'dogs/detail.html', {
        'dog': dog, 
        'feeding_form': FeedingForm,
        'toys': toys_dog_doesnt_have
        })

def add_photo(request, dog_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, dog_id=dog_id)
        except:
            print('An error occurred while uploading file to S3')
    return redirect('detail', dog_id=dog_id)

class DogCreate(CreateView):
    """
    This class will create a dog object
    """
    model = Dog
    fields = ['name', 'breed', 'description', 'age']
    success_url = '/dogs/'

class DogUpdate(UpdateView):
    """
    This class will update a dog object from the DB
    """
    model = Dog
    fields = ['description', 'age']
    
    def get_success_url(self, **kwargs):
        return reverse('detail', args=(self.object.id,))

class DogDelete(DeleteView):
    """
    This class will delete a dog object from the DB
    """
    model = Dog
    success_url = '/dogs/'

def add_feeding(request, dog_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.dog_id = dog_id
        new_feeding.save()
    return redirect('detail', dog_id=dog_id)

def assoc_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.add(toy_id)
    return redirect('detail', dog_id=dog_id)

def unassoc_toy(request, dog_id, toy_id):
    Dog.objects.get(id=dog_id).toys.remove(toy_id)
    return redirect('detail', dog_id=dog_id)

class ToyList(ListView):
    model = Toy

class ToyDetail(DetailView):
    model = Toy

class ToyCreate(CreateView):
    model = Toy
    fields = '__all__'

class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']

class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys/'