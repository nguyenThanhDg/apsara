from rest_framework.serializers import ModelSerializer
from .models import Category, Product, Type


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type