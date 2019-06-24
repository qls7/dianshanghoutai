from rest_framework import serializers

from goods.models import SPU, SPUSpecification, SpecificationOption


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
