from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from users.models import User


class PermsGroupsSimpleSerializer(serializers.ModelSerializer):
    """获取简单用户组列表"""
    class Meta:
        model = Group
        fields = ('id', 'name')


class PermsAdminsSerializer(serializers.ModelSerializer):
    """管理员用户列表序列化器类"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'mobile', 'groups', 'user_permissions')


class PermsSimpleSerializer(serializers.ModelSerializer):
    """获取权限简单列表"""
    class Meta:
        model = Permission
        fields = ('id', 'name')


class PermsGroupSerializer(serializers.ModelSerializer):
    """用户组列表序列化器类"""
    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class PermsTypesSerializer(serializers.ModelSerializer):
    """权限类型列表序列化器类"""

    class Meta:
        model = ContentType
        fields = ('id', 'name')


class PermsSerializer(serializers.ModelSerializer):
    """权限列表序列化器类"""

    class Meta:
        model = Permission
        fields = '__all__'

    def validate_content_type(self, value):
        """校验权限类型"""
        if not ContentType.objects.filter(pk=value.id):
            raise serializers.ValidationError('权限类型错误')
        return value
