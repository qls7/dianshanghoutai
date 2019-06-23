from rest_framework import serializers

from goods.models import SKUImage, SKU, SKUSpecification, SPU, SPUSpecification, SpecificationOption, GoodsCategory


class SPECSSimpleSerializer(serializers.ModelSerializer):
    """规格选项序列化器"""
    spec_id = serializers.IntegerField(label='商品规格id')
    option_id = serializers.IntegerField(label='商品选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class SKUSSerializer(serializers.ModelSerializer):
    """SKU序列化器类"""
    spu = serializers.StringRelatedField(label='商品的spu名称', read_only=True)
    spu_id = serializers.IntegerField(label='商品spu id')
    category = serializers.StringRelatedField(label='三级分类名称', read_only=True)
    category_id = serializers.IntegerField(label='三级分类id')
    specs = SPECSSimpleSerializer(label='规格及选项', many=True)

    class Meta:
        model = SKU
        # fields = '__all__'
        exclude = ('create_time', 'update_time', 'comments', 'default_image')

    def validate(self, attrs):
        """校验spu_id, spec_id, option_id"""
        spu_id = attrs.get('spu_id')
        specs = attrs.get('specs')
        category_id = attrs.get('category_id')
        try:
            spu = SPU.objects.get(id=spu_id)
        except:
            raise serializers.ValidationError('商品spu_id有误')
        if not GoodsCategory.objects.filter(id=category_id, parent__isnull=False):
            raise serializers.ValidationError('商品category_id有误')
        # 校验规格的数量是否完整
        count = spu.specs.all().count()
        if len(specs) < count:
            raise serializers.ValidationError('商品specs不完整')

        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')
            if not SPUSpecification.objects.filter(spu_id=spu_id, id=spec_id):
                raise serializers.ValidationError('商品spec_id有误')
            if not SpecificationOption.objects.filter(spec_id=spec_id, id=option_id):
                raise serializers.ValidationError('商品option_id有误')
        return attrs

    def create(self, validated_data):
        """自定义新增,默认的不支持嵌套写入"""
        specs = validated_data.pop('specs')
        sku = SKU.objects.create(**validated_data)
        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')
            SKUSpecification.objects.create(
                sku=sku, spec_id=spec_id, option_id=option_id
            )
        return sku

    def update(self, instance, validated_data):
        """重写更新, 默认的不支持嵌套更新"""
        specs = validated_data.pop('specs')
        sku = super().update(instance, validated_data)
        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')
            SKUSpecification.objects.create(
                sku=sku, spec_id=spec_id, option_id=option_id
            )
        return sku


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
