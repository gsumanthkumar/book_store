from multiprocessing import set_forkserver_preload
from tokenize import Name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    Name = models.CharField(max_length=20)

    def __str__(self):
        return self.Name

class Book(models.Model):
    Name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

    def __str__(self):
        return self.Name

class Cart(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)

class WishList(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE)
    customer = models.ForeignKey(User,on_delete=models.CASCADE)