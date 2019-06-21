from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel
from meiduo_admin.serializers.channels import GoodsChannelSerializer


class GoodsChannelViewSet(ModelViewSet):
    """频道数据的增删改查"""
    queryset = GoodsChannel.objects.all()
    serializer_class = GoodsChannelSerializer
