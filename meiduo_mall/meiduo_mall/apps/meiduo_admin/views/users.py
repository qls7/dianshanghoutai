from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_admin.serializers.users import AuthorizationSerializer, UserSerializer
from users.models import User


# POST /meiduo_admin/users/
# GET /meiduo_admin/users/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
# @method_decorator(permission_required('users.view_user_api'))
class UsersView(ListAPIView, CreateAPIView):
    """获取用户列表接口"""
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    # queryset = User.objects.all()

    @method_decorator(permission_required('users.view_user_api', raise_exception=True))
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        """重写下查询集,判断是否有关键字"""
        keyword = self.request.query_params.get('keyword')
        if keyword:
            queryset = User.objects.filter(username__contains=keyword, is_staff=False)
        else:
            queryset = User.objects.filter(is_staff=False)

        return queryset


class AuthorizationView(CreateAPIView):
    """验证管理员登录"""
    serializer_class = AuthorizationSerializer
    # queryset = User.objects.all()
    # 管理员还没登录不能加权限
    # permission_classes = [IsAdminUser]

    # def post(self, request):
    #     """验证登录"""
    #     # 获取参数
    #     data = request.data
    #     # 校验参数
    #     serializer = AuthorizationSerializer(data=data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     # 返回
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
