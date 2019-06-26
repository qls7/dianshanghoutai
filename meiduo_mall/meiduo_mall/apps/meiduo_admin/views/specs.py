from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SPUSpecification
from meiduo_admin.serializers.specs import GoodsSpecsSerializer


# GET meiduo_admin/goods/specs/?page=1&pagesize=10
class GoodsSpecsViewSet(ModelViewSet):
    """商品规格增删改查视图集"""
    permission_classes = [IsAdminUser]
    queryset = SPUSpecification.objects.all()
    serializer_class = GoodsSpecsSerializer

    lookup_value_regex = '\d+'

