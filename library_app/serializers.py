from cgitb import lookup
from dataclasses import field
from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = [ 'title', 'author', 'category', 'description', 'published_date', 'language']
        

class AuthorSerializer(serializers.ModelSerializer):
    titles = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['author', 'titles']
    def get_titles(self, book):
        return list(Book.objects.filter(author = book.author).values_list('title', flat=True))
