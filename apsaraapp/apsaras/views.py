from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Product, Type, Image, Tag, Like, Comment, Rating, ProductView, User, Order
from .serializers import CategorySerializer, ProductSerializer, TypeSerializer, ImageSerializer, \
    ProductDetailSerializer, TagSerializer, AuthProductDetailSerializer, CommentSerializer, ProductViewSerializer, \
    UserSerializer, OrderSerializer
from .paginator import BasePagination
from django.http import Http404
from django.db.models import F

from django.conf import settings


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q

    @action(methods=['get'], detail=True, url_path='products')
    def get_products(self, request, pk):
        category = self.get_object()
        products = category.products.filter(active=True)

        kw = request.query_params.get('kw')
        if kw:
            products = products.filter(subject__icontains=kw)

        return Response(data=ProductSerializer(products, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class ProductDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
    pagination_class = BasePagination

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return AuthProductDetailSerializer

    def get_permissions(self):
        if self.action in ['like', 'rating', 'add_comment']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    def get_queryset(self):
        products = Product.objects.filter(active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            products = products.filter(name__contains=q)
        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            products = products.filter(category_id=category_id)
        return products

    @action(methods=['post'], detail=True, url_path='tags')
    def add_tag(self, request, pk):
        try:
            product = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            tags = request.data.get("tags")
            if tags is not None:
                for tag in tags:
                    t, _ = Tag.objects.get_or_create(name=tag)
                    product.tags.add(t)

                product.save()

                return Response(self.serializer_class(product).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        product = self.get_object()
        user = request.user

        l, _ = Like.objects.get_or_create(product=product, user=user)
        l.active = not l.active
        try:
            l.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=AuthProductDetailSerializer(product, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], url_path='rating', detail=True)
    def rating(self, request, pk):
        product = self.get_object()
        user = request.user

        r, _ = Rating.objects.get_or_create(product=product, user=user)
        r.rate = request.data.get('rate', 0)
        try:
            r.save()
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(data=AuthProductDetailSerializer(product, context={'request': request}).data,
                        status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add-comment')
    def add_comment(self, request, pk):
        content = request.data.get('content')
        if content:
            c = Comment.objects.create(content=content, product=self.get_object(), user=request.user)
            return Response(CommentSerializer(c, context={"request": request}).data,
                            status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='views')
    def inc_view(self, request, pk):
        v, created = ProductView.objects.get_or_create(product=self.get_object())
        v.views = F('views') + 1
        v.save()

        return Response(ProductViewSerializer(v).data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='images')
    def get_images(self, request, pk):
        images = self.get_object().images
        return Response(data=ImageSerializer(images, many=True, context={'request': request}).data, status=status.HTTP_200_OK)


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = BasePagination

    def get_queryset(self):
        products = Product.objects.filter(active=True)
        q = self.request.query_params.get('q')
        if q is not None:
            products = products.filter(name__contains=q)
        category_id = self.request.query_params.get('category_id')
        if category_id is not None:
            products = products.filter(category_id=category_id)
        return products


class TypeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Type.objects.filter(active=True)
    serializer_class = TypeSerializer


class ImageViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Image.objects.filter(active=True)
    serializer_class = ImageSerializer


class TagViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Tag.objects.filter(active=True)
    serializer_class = TagSerializer


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'current_user':
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path="current-user", detail=False)
    def current_user(self, request):
        return Response(self.serializer_class(request.user, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class AuthInfo(APIView):
    def get(self, request):
        return Response(settings.OAUTH2_INFOR, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView,
                     generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def destroy(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().destroy(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().partial_update(request, *args, **kwargs)

        return Response(status=status.HTTP_403_FORBIDDEN)


class OrderViewSet(viewsets.ViewSet, generics.RetrieveAPIView, generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def post(self, request, *args, **kwargs):
        if request.user == self.get_object().user:
            return super().post(request, *args, **kwargs)
