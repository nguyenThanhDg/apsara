from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Category, Product, Type, Image, Tag
from .serializers import CategorySerializer, ProductSerializer, TypeSerializer, ImageSerializer, \
    ProductDetailSerializer, TagSerializer
from .paginator import BasePagination
from django.http import Http404
from django.shortcuts import get_object_or_404 as _get_object_or_404


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q


class ProductDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    serializer_class = ProductDetailSerializer
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
                    product.tags.add()

                product.save()

                return Response(data=ProductDetailSerializer(product, context={'request': request}).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)


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