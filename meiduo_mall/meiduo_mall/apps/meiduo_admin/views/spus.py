from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser

from goods.models import SPU, GoodsCategory, SPUSpecification
from meiduo_admin.serializers.channels import GoodsCategoriesSerializer
from meiduo_admin.serializers.spus import SPUSSimpleSerializer, SPUSpecificationSerializer


# GET /meiduo_admin/goods/(?P<pk>\d+)/specs/
class SPUSpecificationView(ListAPIView):
    """获取SPU商品规格信息"""
    permission_classes = [IsAdminUser]
    # queryset = SPUSpecification.objects.all()
    serializer_class = SPUSpecificationSerializer

    pagination_class = None

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return SPUSpecification.objects.filter(spu_id=pk)


class GoodsCategorySimpleView(ListAPIView):
    """获取简单的一级分类"""
    permission_classes = [IsAdminUser]
    queryset = GoodsCategory.objects.filter(parent__isnull=False)
    serializer_class = GoodsCategoriesSerializer

    pagination_class = None


class SPUSSimpleView(ListAPIView):
    """获取简单的SPUS"""
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSSimpleSerializer

    pagination_class = None