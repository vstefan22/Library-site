from typing import List
from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Book
from .forms import AddBook

class ListOfBooks(ListView):
    model = Book
    template_name = 'library_app/index.html'
    context_object_name = 'book'

class AddBookView(CreateView):
    model = Book
    form_class = AddBook
    context_object_name = 'books'
    success_url = '/home/'
    template_name = 'library_app/add_book.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

 
    

