from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('home/', views.ListOfBooks.as_view(), name = 'index'),
    path('add_book/', views.AddBookView.as_view(), name = 'addBook'),
    path('search/', views.Search.as_view(), name = 'search'),
    path('genres/<str:ctg>/', views.GenreList.as_view(), name = 'genres'),
    path('book/<int:pk>/', views.BookDetail.as_view(), name='book'),
    path('read_book/<str:t>/', views.AddReadBookView.as_view(), name= 'add_read_book'),
    path('profile/<slug:slug>/', views.ReadBookDetail.as_view(), name = 'read_books_detail'),
    path('read_books_list/', views.ReadBooksList.as_view(), name = 'read_books_list'),

    # User account functionality
    path('profile/', views.Profile.as_view(), name = 'profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),
    path('login/', views.Login.as_view(), name = 'login'),
    path('register/', views.RegisterPage.as_view(), name = 'register'),
    path('create_profile/', views.CreateProfile.as_view(), name = 'create_profile'),
    path('edit_profile/<slug:slug>/', views.EditProfile.as_view(), name = 'edit_profile'),
   

]
