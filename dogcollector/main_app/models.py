from django.db import models

# Create your models here.
class Dog:
    def __init__(self, name, breed, description, age):
        self.name = name
        self.breed = breed
        self.description = description
        self.age = age

dogs_list = [
    Dog('Cookie', 'Labrador Retriever', 'brown', 4),
    Dog('Frenchie', 'French Bulldog', 'black and white', 2),
    Dog('Orion', 'Siberian Husky', 'white', 0)
]