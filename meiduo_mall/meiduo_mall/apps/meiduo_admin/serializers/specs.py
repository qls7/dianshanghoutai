from rest_framework import serializers

from goods.models import SPUSpecification


class GoodsSpecsSerializer(serializers.ModelSerializer):
    """商品规格序列化器类"""
    spu = serializers.StringRelatedField(label='spu商品名称', read_only=True)
    spu_id = serializers.IntegerField(label='spu商品id', read_only=True)

    class Meta:
        model = SPUSpecification
        exclude =('create_time', 'update_time')