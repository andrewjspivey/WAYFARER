from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import City, Post, Profile


class Register_Form(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()
    current_city = forms.ModelChoiceField(queryset=City.objects.all())

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'current_city']
        

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
        fields = ['first_name', 'last_name', 'username',]

