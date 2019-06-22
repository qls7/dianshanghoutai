from rest_framework import serializers

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory


class GoodsCategoriesSerializer(serializers.ModelSerializer):
    """获取一级和三级分类数据"""

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


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
    # 这里要重新指定category_id和group_id, 默认的的是readonlyField不支持反序列化
    category_id = serializers.IntegerField(label='一级分类id')
    group_id = serializers.IntegerField(label='频道id')

    class Meta:
        model = GoodsChannel
        fields = ('id', 'category_id', 'group_id', 'url', 'sequence',
                  'category', 'group')

    def validate(self, attrs):
        """校验传过来的频道组id和一级分类的id"""
        category_id = attrs['category_id']
        group_id = attrs['group_id']
        count = GoodsCategory.objects.filter(id=category_id, parent=None).count()
        if count <= 0:
            raise serializers.ValidationError('一级分类id错误')
        count = GoodsChannelGroup.objects.filter(id=group_id).count()
        if count <= 0:
            raise serializers.ValidationError('频道id错误')

        return attrs
