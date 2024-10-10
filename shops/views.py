from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Shop
from .forms import ShopForm
import math

class ShopViewSet(viewsets.ViewSet):
    def create(self, request):
        form = ShopForm(request.data)
        if form.is_valid():
            shop = form.save()
            return Response({"id": shop.id}, status=status.HTTP_201_CREATED)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def search(self, request):
        user_lat = float(request.query_params.get('latitude'))
        user_lon = float(request.query_params.get('longitude'))

        shops = Shop.objects.all()
        shop_distances = []

        for shop in shops:
            distance = self.haversine(user_lat, user_lon, shop.latitude, shop.longitude)
            shop_distances.append((shop, distance))

        sorted_shops = sorted(shop_distances, key=lambda x: x[1])
        results = [{"name": shop[0].name, "distance": shop[1]} for shop in sorted_shops]

        return Response(results)

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c 