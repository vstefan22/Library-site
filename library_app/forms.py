from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . import models

# Add book form
class AddBook(ModelForm):
    class Meta:
        model = models.Book
        fields = ['image', 'title', 'description', 'language', 'category', 'published_date']
        widgets = {
            'image':forms.FileInput(),
            'title':forms.TextInput(attrs={'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'cols': 80, 'rows': 20}),
            'language':forms.TextInput(attrs={'placeholder': 'Language'}),
            'category':forms.TextInput(attrs={'placeholder': 'Genre'}),
            'published_date':forms.DateInput(attrs={'placeholder': 'e.g. 1583-01-01'}),

        }
        
class AddReadBookForm(ModelForm):
    class Meta:
        model = models.AddReadBook
        fields = ['describe', 'started_reading']
        
  
# Register user form
class UserRegisterForm(UserCreationForm):
  email = forms.EmailField()

  class Meta:
      model = User
      fields = ['username', 'email', 'first_name', 'last_name']


# User info
class PersonInfo(ModelForm):
    class Meta:
        model = models.Person
        fields = ['profile_pic', 'description', 'city']

    
class EditProfileForm(ModelForm):
    model = User
    fields = ['email', 'first_name', 'last_name']