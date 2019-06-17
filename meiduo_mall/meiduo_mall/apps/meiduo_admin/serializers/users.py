from rest_framework import serializers

from users.models import User


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
