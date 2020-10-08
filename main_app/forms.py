from django.forms import ModelForm
from .models import City, Post, Profile
from django.contrib.auth.models import User




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
        fields = ['user', 'current_city',]

class User_Form(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email',]

