from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification


class SPECSSimpleSerializer(serializers.ModelSerializer):
    """规格选项序列化器"""

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSSerializer(serializers.ModelSerializer):
    """SKU序列化器类"""
    spu = serializers.StringRelatedField(label='spu的商品名称')
    spu_id = serializers.IntegerField(label='商品spu id')
    category = serializers.StringRelatedField(label='三级分类名称')
    category_id = serializers.IntegerField(label='三级分类id')
    specs = SPECSSimpleSerializer(label='规格及选项', many=True)

    class Meta:
        model = SKU
        # fields = '__all__'
        exclude = ('create_time', 'update_time', 'comments', 'default_image')


class SKUSimpleSerializer(serializers.ModelSerializer):
    """SKU简单序列化器类"""

    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUImageSerializer(serializers.ModelSerializer):
    """商品图片序列化器类"""
    sku_id = serializers.IntegerField(label='sku商品ID')
    sku = serializers.StringRelatedField(label='sku商品名称')

    class Meta:
        model = SKUImage
        exclude = ('create_time', 'update_time')
        extra_kwargs = {
            'sku': {'read_only': True}
        }

    def validate_sku_id(self, value):
        """校验sku_id是否存在"""
        sku = SKU.objects.filter(id=value)
        if not sku:
            raise serializers.ValidationError('sku_id错误')
        return value

    def create(self, validated_data):
        """增加默认图片地址"""
        sku_id = validated_data.get('sku_id')
        sku = SKU.objects.get(id=sku_id)
        # create成功返回的是sku_image对象, 如果没有默认图片, 把属性image给默认
        sku_image = super().create(validated_data)
        if not sku.default_image:
            sku.default_image = sku_image.image
            sku.save()
        return sku_image
