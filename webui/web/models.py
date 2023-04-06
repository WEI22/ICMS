from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class USER(models.Model):

    username = models.CharField(("username"), max_length=150, unique=True)
    date_created = models.DateTimeField(("date_created"), default=timezone.now)
    email = models.EmailField(("email"))
    password1 = models.CharField(("password1"), max_length=128)

class IMAGE(models.Model):
    pest = models.CharField(max_length=500)
    location = models.CharField(max_length=200)
    author = models.IntegerField()
    host = models.CharField(max_length=200)
    number = models.IntegerField()
    cum_num = models.IntegerField()
    image = models.ImageField(upload_to='images')
    image_data = models.BinaryField(null=True)
    date_created = models.DateField(default=timezone.now)
    time_created = models.TimeField(default=timezone.now)

    def __str__(self):
        return self.pest