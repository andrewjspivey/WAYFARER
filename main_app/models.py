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
    

class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    content = models.TextField(max_length=500)
    post_date = models.DateTimeField(auto_now_add = True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    def get_date(self):
        time = datetime.now()
        print(time)
        if self.post_date.minute == time.minute:
            return str(self.post_date.second - time.second) + " seconds ago"
        elif self.post_date.hour == time.hour:
            return str(self.post_date.minute - time.minute) + " minutes ago"
        elif self.post_date.day == time.day:
            return str(self.post_date.hour - time.hour) + " hours ago"
        else:
            if self.post_date.month == time.month:
                return str(self.post_date.day - time.day ) + " days ago"
            else:
                if self.post_date.year == time.year:
                    return str( self.post_date.month - time.month ) + " months ago"
        return self.post_date 








    def __str__(self):
        return f"{self.user}'s {self.city.name} Post : {self.title} submitted on {self.post_date} : {self.content}"

    class Meta:
        ordering = ['-post_date']