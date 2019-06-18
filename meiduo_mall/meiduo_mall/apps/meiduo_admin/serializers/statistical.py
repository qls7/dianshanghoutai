from rest_framework import serializers

from goods.models import GoodsVisitCount


class StatisticalGoodsDayViewSerializer(serializers.ModelSerializer):
    """日分类商品访问量序列化器类"""
    category = serializers.StringRelatedField(label='商品分类名称', read_only=True)

    class Meta:
        model = GoodsVisitCount
        fields = ('category', 'count')
        extra_kwargs = {
            'count': {'read_only': True}
        }