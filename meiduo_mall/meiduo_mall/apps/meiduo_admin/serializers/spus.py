from rest_framework import serializers

from goods.models import SPU, SPUSpecification, SpecificationOption, Brand, GoodsCategory


class SPUSSerializer(serializers.ModelSerializer):
    """SPU序列化器类"""
    brand_id = serializers.IntegerField(label='品牌id')
    brand = serializers.StringRelatedField(label='品牌名称', read_only=True)
    category1_id = serializers.IntegerField(label='一级类别')
    category2_id = serializers.IntegerField(label='二级类别')
    category3_id = serializers.IntegerField(label='三级类别')

    class Meta:
        model = SPU
        exclude = ('create_time', 'update_time', 'category1',
                   'category2', 'category3')
        extra_kwargs = {
            'desc_detail': {'allow_blank': True},
            'desc_pack': {'allow_blank': True},
            'desc_service': {'allow_blank': True},
            'comments': {'read_only': True},
            'sales': {'read_only': True},
        }

    def validate(self, attrs):
        """校验品牌id, 一二三级类别"""
        brand_id = attrs.get('brand_id')
        category1_id = attrs.get('category1_id')
        category2_id = attrs.get('category2_id')
        category3_id = attrs.get('category3_id')
        if not Brand.objects.filter(id=brand_id):
            raise serializers.ValidationError('品牌id错误')
        if not GoodsCategory.objects.filter(parent=None, id=category1_id):
            raise serializers.ValidationError('一级分类id错误')
        if not GoodsCategory.objects.filter(parent=category1_id, id=category2_id):
            raise serializers.ValidationError('二级分类id错误')
        if not GoodsCategory.objects.filter(parent=category2_id, id=category3_id):
            raise serializers.ValidationError('三级分类id错误')
        return attrs


class SpecificationOptionSimpleSerializer(serializers.ModelSerializer):
    """简易规格选项序列化器类"""

    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')


class SPUSpecificationSerializer(serializers.ModelSerializer):
    """获取spu商品规格信息序列化器类"""
    spu = serializers.StringRelatedField(label='spu商品名称')
    spu_id = serializers.IntegerField(label='spu商品id')
    options = SpecificationOptionSimpleSerializer(label='选项名称', many=True)

    class Meta:
        model = SPUSpecification
        exclude = ('create_time', 'update_time')


class SPUSSimpleSerializer(serializers.ModelSerializer):
    """简单SPUS序列化器类"""

    class Meta:
        model = SPU
        fields = ('id', 'name')
