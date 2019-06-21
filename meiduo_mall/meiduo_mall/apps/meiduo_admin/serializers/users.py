import re
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户表序列化器类"""

    # keyword = serializers.CharField(label='关键字')

    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')
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
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度为8位',
                    'max_length': '密码最大长度为20位',
                }
            }
        }

    def validate_mobile(self, value):
        """
        自定义手机号检测
        :param value:
        :return:
        """
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式不正确')

        count = User.objects.filter(mobile=value).count()
        if count > 0:
            raise serializers.ValidationError('手机号已经注册,请务重复注册')

        return value

    def create(self, validated_data):
        """
        重写保存用户的create方法
        :param validated_data:
        :return:
        """
        # 用密文进行存储
        user = User.objects.create_user(**validated_data)

        return user


class AuthorizationSerializer(serializers.ModelSerializer):
    """验证序列化器类"""
    token = serializers.CharField(label='JWK token', read_only=True)
    username = serializers.CharField(label='用户名')  # 不能用自带的,会有判断是否重复的字段要用自己的

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            },
        }

    def validate(self, attrs):
        """自定义验证用户名和密码"""
        username = attrs['username']
        password = attrs['password']
        try:
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExit:
            raise serializers.ValidationError('手机号或密码错误')
        if not user.check_password(password):
            raise serializers.ValidationError('手机号或密码错误')

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        """重新增加一个jwt"""
        # 生成jwt token
        user = validated_data['user']
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        user.token = token

        return user
