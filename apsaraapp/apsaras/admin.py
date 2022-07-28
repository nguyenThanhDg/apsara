from django.contrib import admin
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import User, Category, Product, Type, Image, Tag


class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorUploadingWidget)

    class Meta:
        models = Product
        fields = '__all__'


class ProductAdmin(admin.ModelAdmin):
    form = ProductForm
    list_display = ["name", "id", "price", "category", "active", "type", "created_date"]
    search_filter = ["name", "price"]
    list_filter = ["name", "price"]


admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Type)
admin.site.register(Image)
admin.site.register(Tag)