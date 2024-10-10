from django.urls import path, include
from rest_framework.routers import DefaultRouter
from shops.views import ShopViewSet

# Setup a router for the ShopViewSet
router = DefaultRouter()
router.register(r'shops', ShopViewSet, basename='shop')

urlpatterns = [
    path('', include(router.urls)),  # Include all router-defined URLs
]
