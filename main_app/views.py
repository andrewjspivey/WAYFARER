from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import City,Post
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request, 'home.html')


def about(request):
    return HttpResponse( '<h1>About</h1>')


def user_detail(request):
    return render(request, 'profile/detail.html')


def cities_index(request):
    return HttpResponse( '<h1>cities_index</h1>')



def cities_detail(request):
    return HttpResponse( '<h1>cities_detail</h1>')


def cities_delete(request):
    return HttpResponse( '<h1>cities_delete</h1>')

    
def cities_edit(request):
    return HttpResponse( '<h1>cities_edit</h1>')

    
def signup(request):
    return HttpResponse( '<h1>signup</h1>')






