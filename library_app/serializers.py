from cgitb import lookup
from dataclasses import field
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Book
        fields = ['url', 'image', 'title', 'author', 'category', 'description', 'published_date', 'language', 'read_book_count']

