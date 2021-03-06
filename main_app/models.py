from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models.fields import (DateField, DateTimeField, IntegerField, TimeField)
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.

User._meta.get_field('email')._unique = True


# CITY MODEL   (POST: MANY TO MANY)  (USER: ONE TO ONE)
class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# PROFILE MODEL   (POST: ONE PROFILE TO MANY POSTS)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.ImageField(null=True, blank= True, upload_to = 'images/', default='images/default_icon.png')
    slug = models.SlugField(max_length=25, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug= self.slug or slugify(self.user.username)
        return super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('profile_detail', kwargs={'slug':self.slug})

    def __str__(self):
        return f"{self.slug} is currently in {self.current_city}"


# POST MODEL    (POST: MANY TO MANY)
class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True, blank=True, upload_to = 'images/')
    content = models.TextField(max_length=5000 ,blank=False)
    post_date = models.DateTimeField(auto_now_add = True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
 
    def get_date(self):
        cur_time = datetime.now()
        print(cur_time)
        print(self.post_date)
        if self.post_date.day == cur_time.day:
            if cur_time.hour - self.post_date.hour < 1:
                return "Less than an hour ago"
            elif cur_time.hour - self.post_date.hour == 1:
                return "1 hour ago"
            else:
                return str(abs(cur_time.hour  -  self.post_date.hour)) + " hours ago"
        elif self.post_date.month == cur_time.month:
            if cur_time.day - self.post_date.day == 1:
                return "1 day ago"
            else:
                return str(abs(cur_time.day - self.post_date.day)) + " days ago"
        elif self.post_date.year == cur_time.year:
            if cur_time.month - self.post_date.month == 1:
                return "1 month ago"
            else:
                return str(abs(cur_time.month - self.post_date.month)) + " months ago"
        return self.post_date 

    def __str__(self):
        return f"{self.user}'s {self.city.name} Post : {self.title} submitted on {self.post_date} : {self.content}"

    class Meta:
        ordering = ['-post_date']



class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,related_name='comments', on_delete=models.CASCADE)
    text = models.TextField(max_length=500)
    commented_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

    def get_date(self):
        cur_time = datetime.now()
        print(cur_time)
        if self.commented_date.day == cur_time.day:
            if cur_time.hour - self.commented_date.hour < 1:
                return "Less than an hour ago"
            elif cur_time.hour - self.commented_date.hour == 1:
                return "1 hour ago"
            else:
                return str(abs(cur_time.hour  -  self.commented_date.hour)) + " hours ago"
        elif self.commented_date.month == cur_time.month:
            if cur_time.day - self.commented_date.day == 1:
                return "1 day ago"
            else:
                return str(abs(cur_time.day - self.commented_date.day)) + " days ago"
        elif self.commented_date.year == cur_time.year:
            if cur_time.month - self.commented_date.month == 1:
                return "1 month ago"
            else:
                return str(abs(cur_time.month - self.commented_date.month)) + " months ago"
        return self.commented_date
    
    def __str__(self):
        return f"{self.user} made a comment called '{self.post}' on {self.commented_date}"