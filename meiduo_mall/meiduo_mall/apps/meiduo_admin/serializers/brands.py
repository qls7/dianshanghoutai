from rest_framework import serializers

from goods.models import Brand


class GoodsBrandsSerializer(serializers.ModelSerializer):
    """商品品牌序列化器类"""
    class Meta:
        model = Brand
        exclude = ('create_time', 'update_time')


class BrandsSimpleSerializer(serializers.ModelSerializer):
    """简单品牌序列化器类"""
    class Meta:
        model = Brand
        fields = ('id', 'name')
