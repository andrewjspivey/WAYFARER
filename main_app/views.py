from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import City, Post

from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return HttpResponse('<h1>WAYFARER</h1>')

