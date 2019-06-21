from rest_framework import serializers

from goods.models import SKUImage, SKU


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU序列化器类"""
    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器类"""
    sku_id = serializers.IntegerField(label='sku商品ID')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')
