from django.forms import ModelForm
from .models import City, Post

class City_Form(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'image', 'country']

class Post_Form(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'image', 'content']