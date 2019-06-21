from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer


# GET /meiduo_admin/skus/images/?page=<页码>&page_size=<页容量>
class SKUImagesViewSet(ModelViewSet):
    """商品图片的增删改查"""
    permission_classes = [IsAdminUser]
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer
    # 指定动态生成路由时, 提取参数的正则表达式, 可以不写
    lookup_value_regex = '\d+'


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    """简单获取sku列表"""
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer
