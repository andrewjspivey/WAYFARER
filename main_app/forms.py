from django.forms import ModelForm
from .models import City, Post, Profile

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms



class Register_Form(UserCreationForm):
    first_name = forms.CharField()
    class Meta:
        model = User
        fields = ['first_name']
        

    

class City_Form(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'image', 'country']



class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content' ]


class Profile_Form(ModelForm):
    class Meta:
        model = Profile
        fields = ['current_city',]

class User_Form(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',]

