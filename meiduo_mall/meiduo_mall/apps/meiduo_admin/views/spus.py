from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, GoodsCategory, SPUSpecification, Brand
from meiduo_admin.serializers.brands import BrandsSimpleSerializer
from meiduo_admin.serializers.channels import GoodsCategoriesSerializer
from meiduo_admin.serializers.spus import SPUSSimpleSerializer, SPUSpecificationSerializer, SPUSSerializer


# GET /meiduo_admin/goods/?page=1&pagesize=10
class SPUSViewSet(ModelViewSet):
    """SPU视图集"""
    permission_classes = [IsAdminUser]
    queryset = SPU.objects.all()
    serializer_class = SPUSSerializer

    # GET / meiduo_admin / goods / brands / simple /
    def brands_simple(self, request):
        """返回简单的商品品牌"""
        instance = Brand.objects.all()
        serializer = BrandsSimpleSerializer(instance, many=True)
        return Response(serializer.data)

    # GET /meiduo_admin/goods/channel/categories/(?P<pk>\d+)/
    def channel_categories(self, request, pk=None):
        """返回商品分类,第一次返回父类, 再次请求返回二级和三级"""
        if pk:
            instance = GoodsCategory.objects.filter(parent_id=pk)
        else:
            instance = GoodsCategory.objects.filter(parent=None)
        serializer = GoodsCategoriesSerializer(instance, many=True)
        return Response(serializer.data)


# GET /meiduo_admin/goods/(?P<pk>\d+)/specs/
class SPUSpecificationView(ListAPIView):
    """获取SPU商品规格信息"""
    permission_classes = [IsAdminUser]
    queryset = SPUSpecification.objects.all()
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
