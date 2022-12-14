from urllib import request
from django.views.generic import ListView, CreateView, DetailView, FormView, UpdateView, RedirectView
from django.views.generic.edit import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy, reverse
import datetime

from django.shortcuts import HttpResponseRedirect, HttpResponse


from .serializers import AuthorSerializer

from rest_framework.views import APIView
from django.http import Http404

from rest_framework.response import Response
from .permissions import DetailPermission, PostPermission
from .serializers import BookSerializer
from rest_framework import status

from library_app import models
from .models import Book, Person, AddReadBook, SavedBook, Comment, FriendShip, FavouriteBooks
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
            try:
                favourite_books = models.FavouriteBooks.objects.filter(person = self.request.user.person).values_list('book__title', flat = True)
                exc = Book.objects.exclude(title__in = read_books).exclude(id__in = saved_book).exclude(title__in = favourite_books)
            except Person.DoesNotExist:
                exc = Book.objects.exclude(title__in = read_books).exclude(id__in = saved_book)

            context['book'] = exc
            context['book_category'] = book_category
            context['user'] = Book.objects.filter(user = self.request.user)
        else:
             context['book'] = Book.objects.all()
             
        return context


class NewFollowers(ListView):
    model = FriendShip
    template_name = 'friendship_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_date = datetime.date.today()
        new_followers = None
        try:
            new_followers = FriendShip.objects.filter(sent_to = self.request.user.person, date = current_date).distinct('followed_by')
        except:
            HttpResponse("You need to make profile to have access to visit this page.")
        context['new_followers'] = new_followers
        return context

class AddToFavourite(CreateView):
    model = models.FavouriteBooks
    fields = ['book']
    template_name = 'library_app/add_to_favourite.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs['title']
        book = Book.objects.get(title = slug)
        fav_books = None
        try:
            fav_books = self.model.objects.create(book = book, person = self.request.user.person)
        except Person.DoesNotExist:
            HttpResponse("You need to make an account to add books to favourite.")

        context['favourite_books'] = fav_books
        return context


class FavouriteBooks(ListView):
    model = models.FavouriteBooks
    template_name = 'library_app/favourite_books.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        favourite_books = self.model.objects.all().distinct('book')
        context['favourite_books'] = favourite_books
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
            try:
                my_p = Person.objects.get(profile = self.request.user)
            except Person.DoesNotExist:
                return HttpResponse("Create profile, to post a comment")

            form.instance.user = my_p
            form.instance.book = title
            return super().form_valid(form)

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        book = Book.objects.filter(title = self.kwargs['slug'])


        try:
            user = Person.objects.get(profile = self.request.user)
            context['user'] = user
        except Person.DoesNotExist:
            pass
        for i in book:
            title = i
                                
        # sesions 
        current_book_id = Book.objects.filter(title = self.kwargs['slug']).values_list('id', flat = True)

        for i in current_book_id:
            crt = i


        if 'recently_viewed_books' in self.request.session:
            if crt in self.request.session['recently_viewed_books']:
                self.request.session['recently_viewed_books'].remove(crt)
            books_in_session = Book.objects.filter(pk__in = self.request.session['recently_viewed_books'])
            context['books_in_session'] = books_in_session
            self.request.session['recently_viewed_books'].insert(0, crt)
            if (len(self.request.session['recently_viewed_books']))>5:
                self.request.session['recently_viewed_books'].pop()
        else:
            self.request.session['recently_viewed_books'] = [crt]
        
        self.request.session.modified = True

        
        
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
        self.q = Book.objects.filter(category = self.kwargs['ctg'])
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
        i = None
        added_books_count = Person.objects.filter(profile = self.request.user).values_list('added_books_count', flat = True)
        for i in added_books_count:
            i += 1
        
        try:
            update_added_books = Person.objects.filter(profile = self.request.user).update(added_books_count = i)
        except Person.DoesNotExist: 
            pass
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
    
class RemoveReadBook(LoginRequiredMixin, DeleteView):
    model = AddReadBook
    slug_field = 'title'
    success_url = reverse_lazy('index')


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
        book = AddReadBook.objects.filter(user = self.request.user, title = self.kwargs['slug'])
        context['book'] = book
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
            ss_objects = SavedBook.objects.filter(book__id__in = book_q, person = self.request.user).exclude(book__title__in = read_book)
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


class Publisher(DetailView):
    model = Person
    template_name = 'library_app/profile_publisher.html'
    try:
        slug_field = 'profile'
    except:
        raise Http404
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            profile_publisher = Person.objects.filter(profile = self.kwargs['pk'])
            profile_publisher_get = Person.objects.get(profile = self.kwargs['pk'])
            check_user = Person.objects.get(profile = self.kwargs['pk'])

            profile_publisher_followers = FriendShip.objects.filter(sent_to = profile_publisher_get).count()
            profile_publisher_following = FriendShip.objects.filter(followed_by = profile_publisher_get).count()


            profile_publisher_followers_followed_by = FriendShip.objects.filter(sent_to = profile_publisher_get).exclude(followed_by = None)
            
            for follower in profile_publisher_followers_followed_by:
                follower_query = follower.followed_by
                    
            if self.request.user == follower_query.profile:
                context['show'] = True
            else:
                context['show'] = False
            if self.request.user.person:
                context['has_perm'] = True
            else:
                context['has_perm'] = False
            if self.request.user.person:
                if self.request.user.person == check_user:
                    context['check_user'] = True 
                else:
                    context['check_user'] = False
            context['followers'] = profile_publisher_followers
            context['following'] = profile_publisher_following
            context['user_publisher'] = profile_publisher
        except:
            raise Http404
        return context


class Follow(CreateView):
    model = FriendShip
    template_name = 'library_app/follow_profile_publisher.html'
    slug_field = 'id'
    fields = ['followed_by', 'sent_to', 'follow']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        followed_by = self.request.user

        sent_to = Person.objects.get(profile_id = self.kwargs['pk'])
        friendship = FriendShip(
            
            followed_by = followed_by.person,
            
            sent_to = sent_to
        )
        following = FriendShip.objects.create(sent_to = self.request.user.person, follow = sent_to)
        friendship.save()
        following.save()
        person = Person.objects.filter(profile = self.kwargs['pk'])
        followers = FriendShip.objects.filter(followed_by = self.kwargs['pk']).count()
        following = FriendShip.objects.filter(sent_to = self.kwargs['pk']).count()
        context['followers'] = followers
        context['following'] = following
        context['person'] = person
        context['friendship'] = friendship
        
        return context


class ShowPublisherFollowers(ListView):
    model = FriendShip
    template_name = 'library_app/profile_publisher_followers.html'
    #slug_field = 'following'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_publisher_followers = FriendShip.objects.filter(sent_to = self.kwargs['pk']).distinct('followed_by')
        context['profile_publisher_followers'] = profile_publisher_followers
        return context


class ShowPublisherFollowing(ListView):
    model = FriendShip
    template_name = 'library_app/profile_publisher_following.html'
    slug_field = 'followers'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_publisher_following = FriendShip.objects.filter(sent_to = self.kwargs['pk'])
        context['profile_publisher_following'] = profile_publisher_following
        return context


# User functionalities 

# Profile page with user data
class Profile(LoginRequiredMixin, ListView):
    model = Person
    template_name = 'library_app/profile.html'
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        added_books_count = Person.objects.filter(profile = self.request.user).values_list('added_books_count', flat=True)
        read_books_count = AddReadBook.objects.filter(user = self.request.user).count()
            
        if read_books_count == 1 or read_books_count < 5:
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
        # error
        try:
            followers = FriendShip.objects.filter(followed_by = self.request.user.person).count()
            following = FriendShip.objects.filter(sent_to = self.request.user.person).count()
        except Person.DoesNotExist:
            followers = None
            following = None
            
            
        profile = User.objects.all()

        if account:
            context['person'] = account
            context['read_books'] = read_books
            context['read_books_count'] = read_books_count
            context['followers'] = followers
            context['following'] = following
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
    model = Person
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


# REST API

from rest_framework import generics

class BookApiList(generics.ListCreateAPIView):
    
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [PostPermission]


from rest_framework import generics

class BookApiDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [DetailPermission]
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = 'title'

class BookAuthors(APIView):
    def get(self, request):
        author = Book.objects.distinct('author')
        serializer = AuthorSerializer(author, many = True)
        return Response(serializer.data)

class AuthorDetails(APIView):
    def get(self, request, author):
        author = Book.objects.filter(author = author).distinct('author')
        serializer = AuthorSerializer(author, many = True)
        print(serializer.data)
        return Response(serializer.data)


    

