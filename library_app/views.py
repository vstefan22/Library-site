from django.shortcuts import render

def index(request): 
    return render(request, 'library_app/index.html')
