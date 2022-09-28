from django.urls import path, include
from django.contrib.auth.views import LogoutView
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path('home/', views.ListOfBooks.as_view(), name = 'index'),
    path('add_book/', views.AddBookView.as_view(), name = 'addBook'),
    path('search/', views.Search.as_view(), name = 'search'),
    path('genres/<str:ctg>/', views.GenreList.as_view(), name = 'genres'),
    path('book/<slug:slug>/', views.BookDetail.as_view(), name ='book'),
    path('read_book/<str:t>/', views.AddReadBookView.as_view(), name = 'add_read_book'),
    path('read_book_detail/<slug:slug>/', views.ReadBookDetail.as_view(), name = 'read_books_detail'),
    path('read_books_list/', views.ReadBooksList.as_view(), name = 'read_books_list'),
    path('saved/', views.Saved.as_view(), name = 'saved'),
    path('save/<slug:title>/', views.Save.as_view(), name = 'save'),
    path('edit_book/<slug:slug>/', views.EditBook.as_view(), name = 'edit_book'),
    path('remove_saved_book/<slug:slug>/', views.RemoveSavedBook.as_view(), name = 'remove_saved_book'),
    path('remove_read_book/<slug:slug>/', views.RemoveReadBook.as_view(), name = 'remove_read_book'),
    path('profile/<int:pk>/', views.Publisher.as_view(), name  = 'publisher'),
    path('follow/<int:pk>/', views.Follow.as_view(), name = 'follow'),
    path('new_followers', views.NewFollowers.as_view(), name = 'new_followers'),
    path('add_to_favorite/<slug:title>/', views.AddToFavourite.as_view(), name = 'add_to_favorite'),
    path('favourite_books/', views.FavouriteBooks.as_view(), name = 'favourite_books'),
    path('<int:pk>/followers', views.ShowPublisherFollowers.as_view(), name = 'show_publisher_followers'),
    path('<int:pk>/following', views.ShowPublisherFollowing.as_view(), name = 'show_publisher_following'),

    # User account urls
    path('profile/', views.Profile.as_view(), name = 'profile'),
    path('logout/', LogoutView.as_view(next_page = 'login'), name = 'logout'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('register/', views.RegisterPage.as_view(), name = 'register'),
    path('create_profile/', views.CreateProfile.as_view(), name = 'create_profile'),
    path('edit_profile/<int:pk>/', views.EditProfile.as_view(), name = 'edit_profile'),
    path('added_books/', views.AddedBooks.as_view(), name = 'added_books'),
   
    # Rest api urls
    path('library/api/books/', views.BookApiList.as_view(), name = 'api_list'),
    path('library/api/books/<slug:title>/', views.BookApiDetail.as_view(), name = 'book_api_detail'),
    path('library/api/authors/', views.BookAuthors.as_view(), name = 'authors'),
    path('library/api/authors/<slug:author>/', views.AuthorDetails.as_view(), name = 'author_details'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
