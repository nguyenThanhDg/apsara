from urllib.request import AbstractBasicAuthHandler

from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser
from rest_framework.serializers import ModelSerializer


class User(AbstractUser):
    avatar = models.ImageField(null=True, upload_to='users/%Y/%m')


class ModelBase(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(ModelBase):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50, null=False)
    price = models.IntegerField()
    description = RichTextField()
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    type = models.OneToOneField("Type", on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.name


class Type(ModelBase):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Image(ModelBase):
    name = models.CharField(max_length=50, null=False)
    link = models.ImageField(null=True, upload_to='products/%Y/%m')
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Customer(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    username = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)


class ActionBase(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('customer','product')
        abstract = True


class Like(ActionBase):
    active = models.BooleanField(default=False)


class Comment(ActionBase):
    content = models.TextField()


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)



