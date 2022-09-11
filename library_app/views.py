
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, RedirectView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import HttpResponseRedirect
   

from .models import Book, Person, AddReadBook, SavedBook, Comment
from .forms import AddBook, PersonInfo, UserRegisterForm, AddReadBookForm, EditProfileForm, EditBookForm, CommentForm


# Home page
class ListOfBooks(ListView):
    model = Book
    template_name = 'library_app/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            book_q = Book.objects.filter().values_list('id', flat = True)
            saved_book = SavedBook.objects.filter(book__id__in = book_q, person = self.request.user).values_list('book__id')
            
            read_books = AddReadBook.objects.filter(user = self.request.user).values_list('title', flat=True)
            book_category = Book.objects.all().distinct('category')
            
            exc = Book.objects.exclude(title__in = read_books).exclude(id__in = saved_book)

            context['book'] = exc
            context['book_category'] = book_category
            context['user'] = Book.objects.filter(user = self.request.user)
        else:
             context['book'] = Book.objects.all()
             
        return context


# Single page for book
class BookDetail(DetailView, CreateView, RedirectView):
    model = Book
    form_class = CommentForm
    context_object_name = 'book'
    slug_field = 'title'
    success_url = './'
    
    
    template_name = 'library_app/book.html'
    
    def form_valid(self, form):
        if self.request.user.is_authenticated:
            book = Book.objects.filter(title = self.kwargs['slug'])
            for i in book:
                title = i
            my_p = Person.objects.get(profile = self.request.user)
            form.instance.user = my_p
            form.instance.book = title
            return super().form_valid(form)

            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.filter(title = self.kwargs['slug'])
        if self.request.user.is_authenticated:
            user = Person.objects.get(profile = self.request.user)
            context['user'] = user
        for i in book:
            title = i
        comment_show = Comment.objects.filter(book = title)
        comment_count = Comment.objects.filter(book = title).count()
        context['comments'] = comment_show
        
        context['comment_count'] = comment_count
        return context
    

# Functionlity for genre search from home page
class GenreList(ListView):
    model = Book
    template_name = 'library_app/categories.html'
    
    def get_queryset(self):
        self.ctg = self.kwargs['ctg']
        self.q = Book.objects.filter(category__icontains=self.kwargs['ctg'])
        if self.q:
            object_list = self.q
        else:
            object_list = self.model.objects.none()
        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['result'] = self.object_list
        context['genre'] = self.ctg
        return context


# Add book 
class AddBookView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    
    model = Book
    form_class = AddBook
    context_object_name = 'books'
    success_url = '/home/'
    template_name = 'library_app/add_book.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        added_books_count = Person.objects.filter(profile = self.request.user).values_list('added_books_count', flat = True)
        for i in added_books_count:
            i += 1
        
        update_added_books = Person.objects.filter(profile = self.request.user).update(added_books_count = i)
        return super().form_valid(form)


class EditBook(LoginRequiredMixin, UpdateView):
    template_name = 'library_app/edit_book.html'
    model = Book
    form_class = EditBookForm
    success_url = '/home/'
    slug_field = 'title'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)



class AddReadBookView(LoginRequiredMixin, CreateView):
    model = AddReadBook
    form_class = AddReadBookForm
    template_name = 'library_app/add_read_book.html'
    success_url = '/home/'
        
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.title = self.kwargs['t']
        read_books_count = Book.objects.values_list('read_book_count', flat = True)
        for i in read_books_count:
            i += 1
        
        read_books = Book.objects.filter().update(read_book_count = i)
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.kwargs['t']
        return context

class RemoveSavedBook(LoginRequiredMixin, DeleteView):
    model = SavedBook
    slug_field = 'book__title'
    success_url = reverse_lazy('index')
    def get_object(self, queryset = None):
        if queryset is None:
            queryset = self.get_queryset()

        user = self.request.user
        book = self.kwargs['slug']
        queryset = SavedBook.objects.filter(person = user, book__title = book)
        if not queryset:
            raise Http404
        context = {'user':user, 'book':book}
        return context

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        book = self.kwargs['slug']
        saved_book_delete = SavedBook.objects.filter(person = user, book__title = book)
        saved_book_delete.delete()
        return HttpResponseRedirect(reverse('index', ))
    

class RemoveReadBook(LoginRequiredMixin, DeleteView):
    model = AddReadBook
    slug_field = 'title'
    success_url = reverse_lazy('index')
    def get_object(self, queryset = None):
        if queryset is None:
            queryset = self.get_queryset()

        user = self.request.user
        book = self.kwargs['slug']
        queryset = AddReadBook.objects.filter(user = user, title = book)
        if not queryset:
            raise Http404
        context = {'user':user, 'book':book}
        return context

    def delete(self, request, *args, **kwargs):
        user = self.request.user
        book = self.kwargs['slug']
        saved_book_delete = AddReadBook.objects.filter(user = user, title = book)
        saved_book_delete.delete()
        read_books_count = Book.objects.values_list('read_book_count', flat=True)
        for i in read_books_count:
            i -= 1
        
        read_books = Book.objects.filter().update(read_book_count = i)
        return HttpResponseRedirect(reverse('index', ))

# Searching book
class Search(ListView):
    model = Book
    template_name = 'libarary_app/book_list.html'

    def get_queryset(self):
        self.q = self.request.GET.get('search')

        if self.q:
            object_list = self.model.objects.filter(title__icontains = self.q)

        else:
            object_list = self.model.objects.none()

        return object_list

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            for i in self.object_list:
                obj_title = i
            book_q = Book.objects.filter().values_list('id', flat=True)
            saved_book = SavedBook.objects.filter(book__id__in = book_q, person = self.request.user).values_list('book__id')
            
            read_books = AddReadBook.objects.filter(user = self.request.user).values_list('title', flat=True)
            
            
            exc = Book.objects.filter(title__icontains = self.q).exclude(title__in = read_books).exclude(id__in = saved_book)

            context['result'] = exc
 
        else:
             context['result'] = self.object_list
     
 
        for i in self.object_list:
            if str(i) in exc:
                messages.info(self.request, "Book that you searched is either saved or read by you try searching it in 'Saved' or 'Read' link in side menu ")
                break

        context['result'] = exc
        
        return context


class ReadBookDetail(LoginRequiredMixin, DetailView):
    model = AddReadBook
    template_name = 'library_app/detail_read_book.html'
    slug_field = 'title'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = AddReadBook.objects.filter(user = self.request.user, title = self.kwargs['slug'])
        return context


class ReadBooksList(LoginRequiredMixin, ListView):
    model = AddReadBook
    template_name = 'library_app/read_books_list.html'
    def get_queryset(self):
        self.q = self.request.GET.get('search')

        if self.q:
            object_list = self.model.objects.filter(user = self.request.user, title__icontains = self.q)

        else:
            object_list = self.model.objects.none()

        return object_list
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = AddReadBook.objects.filter(user = self.request.user)
        context['searched_data'] = self.object_list
        return context


class Saved(LoginRequiredMixin, ListView):
    model = SavedBook
    template_name = 'library_app/saved.html'
    def get_queryset(self):
        self.q = self.request.GET.get('search')
        if self.q:
            read_book = AddReadBook.objects.filter(user = self.request.user).values_list('title', flat=True)
            book_q = Book.objects.filter(title__icontains = self.q).values_list('id', flat=True)
            ss_objects = SavedBook.objects.filter(book__id__in = book_q, person = self.request.user).exclude(book__title__in = self.read_book)
            object_list = ss_objects
        
        else:
            read_book = AddReadBook.objects.filter(user = self.request.user).values_list('title', flat=True)
            object_list = SavedBook.objects.filter(person = self.request.user).exclude(book__title__in = read_book)
            if not object_list:
                messages.info(self.request, 'Congratulations! You read every book that you saved!')
            
        return object_list
            
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['object_list'] = self.object_list
        

        
        return context


class Save(LoginRequiredMixin, CreateView):
    model = SavedBook
    fields = ['person', 'book']
    template_name = 'library_app/saved.html'

    def get_context_data(self,**kwargs):
        title = self.kwargs['title']
        book = Book.objects.get(title = title)
        saved_book_ = SavedBook.objects.create(book = book, person = self.request.user)
        saved_book_.save()
        messages.success(self.request, 'Book saved successfully!')


# User functionalities 

# Profile page with user data
class Profile(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'library_app/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_books_count = Person.objects.filter(profile = self.request.user).values_list('added_books_count', flat=True)
        read_books_count = AddReadBook.objects.filter(user = self.request.user).count()
        print(read_books_count)
        if read_books_count == 1 or i < 5:
            context['starter'] = 1
        if read_books_count > 5:
            context['junior_reader'] = 5
        if read_books_count > 15:
            context['informed'] = 15
        if read_books_count > 30:
            context['educated'] = 30
        if read_books_count > 50:
            context['knowledgeable'] = 50
        if read_books_count > 75:
            context['greate_reader'] = 75
        if read_books_count > 100:
            context['genius'] = 100
        for i in added_books_count:
            
            if i == 1 or i<5:
                context['junior'] = 1
            if i > 5:
                context['reader'] = 2
            if i > 15:
                context['experienced_reader'] = 3
            if i > 30:
                context['genius'] = 4
        account = Person.objects.filter(profile = self.request.user)
        read_books = AddReadBook.objects.filter(user = self.request.user)[:3]
        
        profile = User.objects.all()

        if account:
            context['person'] = account
            context['read_books'] = read_books
            context['read_books_count'] = read_books_count

        else:
            context['profile'] = profile
            
        return context


class AddedBooks(ListView):
    model = Book
    template_name = 'library_app/added_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_books = Book.objects.filter(user = self.request.user)
        context['added_books'] = added_books
        return context
# Log in functionality
class Login(LoginView):
    template_name = 'library_app/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('index')

# Register functionality
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


class CreateProfile(LoginRequiredMixin, CreateView):
    model = Profile
    form_class = PersonInfo
    template_name = 'library_app/create_profile.html'
    success_url = '/profile/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.profile  = self.request.user
        form.save()
        return super().form_valid(form)


class EditProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = EditProfileForm
    template_name = 'library_app/edit_profile.html'
    success_url = '/profile/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
        


    

