from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializers.brands import GoodsBrandsSerializer


# meiduo_admin/brands/
class GoodsBrandsViewSet(ModelViewSet):
    """商品品牌视图集"""
    permission_classes = [IsAdminUser]
    queryset = Brand.objects.all()
    serializer_class = GoodsBrandsSerializer
    lookup_value_regex = '\d+'
