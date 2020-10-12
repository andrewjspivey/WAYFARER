from django.db import models
from django.contrib.auth.models import User
from datetime import datetime 
from django.db.models.fields import (DateField, DateTimeField, IntegerField, TimeField)


# Create your models here.


class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    country = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.name}, {self.country}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_city = models.ForeignKey(City, on_delete=models.CASCADE)
    image = models.CharField(max_length=300, default='https://icons-for-free.com/iconfiles/png/512/people+person+profile+user+icon-1320186207447274965.png')
    




class Post(models.Model):
    title = models.CharField(max_length=200)
    image = models.CharField(max_length=250)
    content = models.TextField(max_length=5000 ,blank=False)
    post_date = models.DateTimeField(auto_now_add = True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

 
    def get_date(self):
        cur_time = datetime.now()
        if self.post_date.day == cur_time.day:
                return str(abs(cur_time.hour  -  self.post_date.hour)) + " hours ago"
        elif self.post_date.month == cur_time.month:
                return str(abs(cur_time.day - self.post_date.day)) + " days ago"
        elif self.post_date.year == cur_time.year:
                return str(abs(cur_time.month - self.post_date.month)) + " months ago"
        return self.post_date 




    def __str__(self):
        return f"{self.user}'s {self.city.name} Post : {self.title} submitted on {self.post_date} : {self.content}"

    class Meta:
        ordering = ['-post_date']
    



