from rest_framework import serializers

from goods.models import Brand


class BrandsSimpleSerializer(serializers.ModelSerializer):
    """简单品牌序列化器类"""
    class Meta:
        model = Brand
        fields = ('id', 'name')
