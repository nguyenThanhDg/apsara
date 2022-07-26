from django.shortcuts import render
from rest_framework import viewsets, generics
from .models import Category, Product, Type
from .serializers import CategorySerializer, ProductSerializer, TypeSerializer


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def get_queryset(self):
        q = self.queryset

        kw = self.request.query_params.get('kw')
        if kw:
            q = q.filter(name__icontains=kw)

        return q


class ProductViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Product.objects.filter(active=True)
    serializer_class = ProductSerializer


class TypeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Type.objects.filter(active=True)
    serializer_class = TypeSerializer