from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, Product, Type, Image, Tag


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "category", "type", "created_date"]


class TypeSerializer(ModelSerializer):
    class Meta:
        model = Type
        exclude = ["updated_date"]


class ImageSerializer(ModelSerializer):
    link = serializers.SerializerMethodField(source='link')

    def get_link(self, obj):
        request = self.context['request']
        path = '/static/%s' % obj.link.name

        return request.build_absolute_uri(path)

    class Meta:
        model = Image
        fields = ['id', 'name', 'created_date', 'link', 'product_id']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class ProductDetailSerializer(ProductSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = Product
        fields = ProductSerializer.Meta.fields + ['description', 'tags']