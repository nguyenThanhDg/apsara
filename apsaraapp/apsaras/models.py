
from ckeditor.fields import RichTextField
from django.db import models
from django.contrib.auth.models import AbstractUser
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
    category = models.ForeignKey(Category,related_name='products', null=True, on_delete=models.SET_NULL)
    type = models.ForeignKey("Type", null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag')

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


class ActionBase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user','product')
        abstract = True


class Like(ActionBase):
    active = models.BooleanField(default=False)


class Comment(ActionBase):
    content = models.TextField()

    def __str__(self):
        return self.content


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    price = models.IntegerField(null=True)
    quantity = models.IntegerField(null=True)


class Tag(ModelBase):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Rating(ActionBase):
    rate = models.SmallIntegerField(default=0)


class ProductView(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    views = models.IntegerField(default=0)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)

