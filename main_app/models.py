from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.fields import (DateField, DateTimeField, IntegerField, TimeField)

# Create your models here.

# we may want to add a profile model to supplement user data, decorations (date joined)a


class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    country = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.name}, {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_city = models.ForeignKey(City, on_delete=models.CASCADE)
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    content = models.TextField(max_length=500)
    post_date = models.DateField(auto_now_add = True)
    
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user}'s {self.city.name} Post : {self.title} submitted on {self.post_date} : {self.content}"

    class Meta:
        ordering = ['-post_date']