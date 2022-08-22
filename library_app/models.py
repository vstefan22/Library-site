from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from django.db import models


class Person(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(default='Nana.jpg', upload_to = 'images/', null=True, blank=True)
    description = models.TextField(max_length=950, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    read_books = models.IntegerField(default=0)
    read_books_list = ArrayField(ArrayField(models.CharField(max_length=100, null=True, blank=True),),)




class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default="Nana.jpg", upload_to = 'images/', null = True, blank = True)
    title = models.CharField(max_length=150, unique=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    read = models.BooleanField(default=False)
    started_reading = models.DateField(null=True, blank=True)
    finished_reading = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True, default="Not selected")

    def __str__(self):
        return self.title
        


