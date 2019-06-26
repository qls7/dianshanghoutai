from django import http
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import SpecificationOption, SPUSpecification
from meiduo_admin.serializers.options import SpecOptionsSerializer


# GET /meiduo_admin/specs/options/
class SpecOptionsViewSet(ModelViewSet):
    """规格选项视图集"""
    permission_classes = [IsAdminUser]
    queryset = SpecificationOption.objects.all()
    serializer_class = SpecOptionsSerializer
    lookup_value_regex = '\d+'

    # /meiduo_admin/goods/specs/simple/
    def simple(self, request):
        """获取简单的规格列表"""
        # 构造不重复的规格列表
        name_list = []
        specs_list = []
        all_name = SPUSpecification.objects.values('name', 'id')
        for spec in all_name:
            if spec['name'] not in name_list:
                name_list.append(spec['name'])
                specs_list.append(spec)

        return http.JsonResponse(specs_list, safe=False)