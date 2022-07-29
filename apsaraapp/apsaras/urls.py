from django.contrib import admin
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(prefix='categories', viewset=views.CategoryViewSet, basename='category')
router.register(prefix='products', viewset=views.ProductDetailViewSet, basename='productDetail')
router.register(prefix='products', viewset=views.ProductViewSet, basename='product')
router.register(prefix='types', viewset=views.TypeViewSet, basename='type')
router.register(prefix='images', viewset=views.ImageViewSet, basename='image')
router.register(prefix='users', viewset=views.UserViewSet, basename='user')
router.register(prefix='comments', viewset=views.CommentViewSet, basename='comment')
router.register(prefix='orders', viewset=views.OrderViewSet, basename='order')
urlpatterns = [
    path('', include(router.urls)),
    path('oauth2-info/', views.AuthInfo.as_view())
]