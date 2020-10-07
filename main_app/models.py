from django.db import models

# Create your models here.
    

class City(models.Model):
    name = models.CharField(max_length=50)
    image = models.CharField(max_length=250)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class Post(models.Model):
    title = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    content = models.TextField(max_length=500)
    post_date = models.DateField()
    
    city = models.ForeignKey(City, on_delete=models.CASCADE)


    def __str__(self):
        return self.name