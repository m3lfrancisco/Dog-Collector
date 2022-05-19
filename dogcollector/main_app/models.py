from django.db import models
from django.urls import reverse


MEALS = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class Toy(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('toys_detail', kwargs={'pk':self.id})
    
    def __str__(self):
        return self.name


class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100) 
    description = models.TextField(max_length=250)
    age = models.IntegerField()
    toys = models.ManyToManyField(Toy)

    def __str__(self):
        return self.name


class Feeding(models.Model):
    date = models.DateField('Feeding date')
    meal = models.CharField(
        max_length=1,
        choices=MEALS,
        default=MEALS[0][0]
        )

    def __str__(self):
        return f"{self.get_meal_display()} on {self.date}"

    dog = models.ForeignKey(Dog, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']