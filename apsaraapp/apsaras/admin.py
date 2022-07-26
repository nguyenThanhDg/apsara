from django.contrib import admin

from .models import User, Category, Product, Type

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Type)