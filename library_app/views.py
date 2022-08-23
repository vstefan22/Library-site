from http.client import HTTPResponse
from unicodedata import category
from django.shortcuts import render
from django.views.generic import ListView, CreateView, DetailView, FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.utils.text import slugify

from .models import Book, Person
from .forms import AddBook, UserRegisterForm


class ListOfBooks(ListView):
    model = Book
    template_name = 'library_app/index.html'
    

    context_object_name = 'book'

class GenreList(ListView):
    model = Book
    template_name = 'library_app/categories.html'
    
    def get_queryset(self):
        q = Book.objects.filter(category__icontains=self.kwargs['ctg'])
        print(q)
        if q:
            object_list = q
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.object_list
        return context
    '''
    def get_context_data(self, **kwargs):
        type = self.request.GET.get('category')
        q = Book.objects.filter(category__icontains = type)
        context = super().get_context_data(**kwargs)
        context['genre'] = q
        print(q)
        return context
    '''
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
    model = Person
    template_name = 'library_app/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        account = Person.objects.filter(profile = self.request.user)
        profile = User.objects.all()
        if account:
            context['person'] = account
        else:
            context['profile'] = profile
        print(account)
        #account_city = account.city
        
            
        return context

class Login(LoginView):
    template_name = 'library_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    def get_success_url(self):
        return reverse_lazy('index')

class BookDetail(DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'library_app/book.html'

class RegisterPage(FormView):
    template_name = 'library_app/register.html'
    form_class = UserRegisterForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')


    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)


    

