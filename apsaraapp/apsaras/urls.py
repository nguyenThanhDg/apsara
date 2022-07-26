from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='categories', viewset=views.CategoryViewSet, basename='category')
router.register(prefix='products', viewset=views.ProductViewSet, basename='product')
router.register(prefix='types', viewset=views.TypeViewSet, basename='type')

urlpatterns = [
    path('', include(router.urls)),
]