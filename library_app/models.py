from xml.etree.ElementInclude import default_loader
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

from django.db import models


class AddReadBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    describe = models.TextField()
    started_reading = models.DateField()
    finished_reading = models.DateField(null=True, blank=True)


class Person(models.Model):
    profile = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    profile_pic = models.ImageField(default='Nana.jpg', upload_to = 'images/', null=True, blank=True)
    description = models.TextField(max_length=950, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    added_books_count = models.IntegerField(default=0)
    


class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(default="Nana.jpg", upload_to = 'images/', null = True, blank = True)
    title = models.CharField(max_length=150, unique=True)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField(max_length=5000, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=100, null=True, blank=True, default="Not selected")
    read_book_count = models.IntegerField(default = 0)


    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    comment = models.TextField()
    date = models.DateField(auto_now_add=True)



class SavedBook(models.Model):
    person = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, default="", null=True)
   



        


