from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.channels import GoodsChannelSerializer, GoodsChannelTypesSerializer, \
    GoodsCategoriesSerializer


# GET /meiduo_admin/goods/categories/
class GoodsChannelCategoriesView(ListAPIView):
    """获取一级分类数据"""
    permission_classes = [IsAdminUser]
    queryset = GoodsCategory.objects.filter(parent=None)
    serializer_class = GoodsCategoriesSerializer

    pagination_class = None  # 关闭分页器


class GoodsChannelTypesView(ListAPIView):
    """获取频道组数据"""
    permission_classes = [IsAdminUser]
    queryset = GoodsChannelGroup.objects.all()
    serializer_class = GoodsChannelTypesSerializer

    pagination_class = None  # 关闭分页器


class GoodsChannelViewSet(ModelViewSet):
    """频道数据的增删改查"""
    permission_classes = [IsAdminUser]
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelSerializer

    lookup_value_regex = '\d+'
