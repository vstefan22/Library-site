from unicodedata import name
from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from . import views

urlpatterns = [
    path('home/', views.ListOfBooks.as_view(), name = 'index'),
    path('add_book/', views.AddBookView.as_view(), name = 'addBook'),
    path('search/', views.Search.as_view(), name = 'search'),
    path('profile/', views.Profile.as_view(), name = 'profile'),
    path('logout/', LogoutView.as_view(next_page='login'), name = 'logout'),
    path('login/', views.Login.as_view(), name = 'login'),

]
