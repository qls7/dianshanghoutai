from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers


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
