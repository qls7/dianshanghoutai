import re
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from users.models import User


class PermsAdminsSerializer(serializers.ModelSerializer):
    """管理员用户列表序列化器类"""
    username = serializers.CharField(label='用户名')

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'mobile', 'groups', 'user_permissions')
        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名最小长度为8位',
                    'max_length': '用户名最大长度为20位',
                }
            },
            'password': {
                'write_only': True,
                'required': False,
                'allow_blank': True,
            }
        }

    def validate_mobile(self, value):
        """校验手机号格式"""
        if self.context.get('view').action == 'create':
            if not re.match(r'^1[3-9]\d{9}$', value):
                raise serializers.ValidationError('手机号格式不正确')
            count = User.objects.filter(mobile=value).count()
            if count > 0:
                raise serializers.ValidationError('手机号已经注册,请务重复注册')
        elif self.context.get('view').action == 'update':
            # pk = self.context.get('view').data
            count = User.objects.filter(mobile=value).count()
            if count > 0:
                if value != self.instance.mobile:
                    raise serializers.ValidationError('手机号已经注册,请重新修改')
        return value

    def validate_username(self, value):
        """如果是更新数据, 用户名不用判断重复"""
        if self.context.get('view').action == 'create':
            if User.objects.filter(username=value):
                raise serializers.ValidationError('用户名重复')
        return value

    def create(self, validated_data):
        """密码要加密保存"""
        # 不能直接用create_user manytomany的表结构,不会帮你自动新增的,需要用他自带的create
        # user = User.objects.create_user(**validated_data)
        validated_data['is_staff'] = True
        user = super().create(validated_data)
        password = validated_data.get('password')
        if not password:
            password = '123abc'
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """密码要加密存储"""
        password = validated_data.pop('password')
        super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance


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
