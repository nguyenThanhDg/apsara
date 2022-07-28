from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from .models import Category, Product, Type, Image, Tag, Comment, User, Rating, ProductView


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


class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content', 'product', 'customer']


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='avatar')

    def get_avatar(self, obj):
        request = self.context['request']
        if obj.avatar and not obj.avatar.name.startswith("/static"):

            path = '/static/%s' % obj.avatar.name

            return request.build_absolute_uri(path)

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name',
                  'username', 'password', 'email',
                  'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        exclude = ['active']


class AuthProductDetailSerializer(ProductDetailSerializer):
    like = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()

    def get_like(self, product):
        request = self.context.get('request')
        if request:
            return product.like_set.filter(user=request.user, active=True).exists()

    def get_rating(self, product):
        request = self.context.get('request')
        if request:
            r = product.rating_set.filter(user=request.user).first()
            if r:
                return r.rate

    class Meta:
        model = Product
        fields = ProductDetailSerializer.Meta.fields + ['like', 'rating']


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rate', 'created_date']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'active', 'created_date']


class ProductViewSerilizer(ModelSerializer):
    class Meta:
        model = ProductView
        fields = ['id', 'views', 'product']