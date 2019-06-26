from rest_framework import serializers

from goods.models import SPUSpecification, SPU


class GoodsSpecsSerializer(serializers.ModelSerializer):
    """商品规格序列化器类"""
    spu = serializers.StringRelatedField(label='spu商品名称', read_only=True)
    spu_id = serializers.IntegerField(label='spu商品id')

    class Meta:
        model = SPUSpecification
        exclude =('create_time', 'update_time')

    def validate_spu_id(self, value):
        """校验spu_id存不存在"""
        if not SPU.objects.filter(pk=value):
            raise serializers.ValidationError('spu_id错误')
        return value