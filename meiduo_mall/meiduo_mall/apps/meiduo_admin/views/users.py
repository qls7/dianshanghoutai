from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_admin.serializers.users import AuthorizationSerializer
from users.models import User


class AuthorizationView(CreateAPIView):
    """验证管理员登录"""
    serializer_class = AuthorizationSerializer
    queryset = User.objects.all()
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
