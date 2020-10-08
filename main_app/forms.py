from django.forms import ModelForm
from .models import City, Post



class City_Form(ModelForm):
    class Meta:
        model = City
        fields = ['name', 'image', 'country']

       

