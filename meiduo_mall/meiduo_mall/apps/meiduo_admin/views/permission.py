from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.permission import PermsSerializer, PermsTypesSerializer


# GET / meiduo_admin / permission / perms /
class PermsViewSet(ModelViewSet):
    """用户权限列表增删改查视图集"""
    permission_classes = [IsAdminUser]
    queryset = Permission.objects.all()
    serializer_class = PermsSerializer


# GET / meiduo_admin / permission / content_types /
class PermsTypesView(ListAPIView):
    """获取权限类型列表"""
    permission_classes = [IsAdminUser]
    queryset = ContentType.objects.all()
    serializer_class = PermsTypesSerializer

    pagination_class = None
