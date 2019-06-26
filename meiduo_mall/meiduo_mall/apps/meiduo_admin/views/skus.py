from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSSerializer


# GET /meiduo_admin/skus/?keyword=<名称|副标题>&page=<页码>&page_size=<页容量>
class SKUSViewSet(ModelViewSet):
    """skus视图集,sku的增删改查"""
    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSSerializer

    lookup_value_regex = '\d+'

    def get_queryset(self):
        """判断是否有keyword关键字查询"""
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))

        return SKU.objects.all()


# GET /meiduo_admin/skus/simple/
class SKUSimpleView(ListAPIView):
    """简单获取sku列表"""
    pagination_class = None

    permission_classes = [IsAdminUser]
    queryset = SKU.objects.all()
    serializer_class = SKUSimpleSerializer


# GET /meiduo_admin/skus/images/?page=<页码>&page_size=<页容量>
class SKUImagesViewSet(ModelViewSet):
    """商品图片的增删改查"""
    permission_classes = [IsAdminUser]
    queryset = SKUImage.objects.all()
    serializer_class = SKUImageSerializer
    # 指定动态生成路由时, 提取参数的正则表达式, 可以不写
    lookup_value_regex = '\d+'
