from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth.models import User
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

class Search(ListView):
    model = Book
    template_name = 'libarary_app/book_list.html'

    def get_queryset(self):
        q = self.request.GET.get('search')
        if q:
            object_list = self.model.objects.filter(title__icontains = q)
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.object_list
        return context

class Profile(ListView):
    model = User
    template_name = 'library_app/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_info'] = self.request.user
        return context
 
    

