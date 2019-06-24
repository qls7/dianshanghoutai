from django.contrib.auth.models import Permission, Group
from users.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from meiduo_admin.serializers.permissions import PermsSerializer, PermsTypesSerializer, PermsGroupSerializer, \
    PermsSimpleSerializer, PermsAdminsSerializer


# GET /meiduo_admin/permission/admins/
class PermsAdminsViewSet(ModelViewSet):
    """管理员的增删改查"""
    permission_classes = [IsAdminUser]
    queryset = User.objects.filter(is_staff=True)
    serializer_class = PermsAdminsSerializer

    # GET / meiduo_admin / permission / groups / simple /
    def simple(self, request):
        """获取简单用户组"""
        instance = Group.objects.all()
        serializer = PermsGroupSerializer(instance, many=True)
        return Response(serializer.data)


# GET /meiduo_admin/permission/groups/
class PermsGroupViewSet(ModelViewSet):
    """权限组列表的增删改查"""
    permission_classes = [IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = PermsGroupSerializer

    # GET / meiduo_admin / permission / simple /
    # @action(methods=['get'], detail=False) 路径不合适不能自动生成需要手动添加
    def simple(self, request):
        """获取权限列表"""
        instance = Permission.objects.all()
        serializer = PermsSimpleSerializer(instance=instance, many=True)
        return Response(serializer.data)


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
