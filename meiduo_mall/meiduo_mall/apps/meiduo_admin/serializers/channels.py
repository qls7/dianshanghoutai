from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup


# GET /meiduo_admin/goods/channel_types/
class GoodsChannelTypesSerializer(serializers.ModelSerializer):
    """商品频道组序列化器类"""
    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')


# GET /meiduo_admin/goods/channels/?page=<页码>&page_size=<页容量>
class GoodsChannelSerializer(serializers.ModelSerializer):
    """商品频道序列化器类"""
    category = serializers.StringRelatedField(label='一级分类名称')
    group = serializers.StringRelatedField(label='频道组名称')

    class Meta:
        model = GoodsChannel
        fields = ('id', 'category_id', 'group_id', 'url', 'sequence',
                  'category', 'group')