from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrdersUpdateSerializer(serializers.ModelSerializer):
    """修改订单商品的序列化器类"""
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'status')
        read_only_fields =('order_id', )

    def validate_status(self, value):
        """校验status的值"""
        if 1 <= int(value) <= 6:
            return value
        else:
            raise serializers.ValidationError('status值错误')


class OrderSKUSerializer(serializers.ModelSerializer):
    """订单商品sku序列化器类"""
    class Meta:
        model = SKU
        fields = ('name', 'default_image')


class OrderGoodsSerializer(serializers.ModelSerializer):
    """订单商品序列化器类"""
    sku = OrderSKUSerializer(label='订单sku详情')

    class Meta:
        model = OrderGoods
        fields = ('count', 'price', 'sku')


class OrdersDetailViewSerializer(serializers.ModelSerializer):
    """订单详情序列化器类"""
    create_time = serializers.DateTimeField(label='创建时间', format='%Y-%m-%d %H:%M:%S')
    user = serializers.StringRelatedField(label='下单用户名')
    skus = OrderGoodsSerializer(label='商品列表', many=True)

    class Meta:
        model = OrderInfo
        exclude = ('update_time', 'address')


class OrdersViewSerializer(serializers.ModelSerializer):
    """订单管理序列化器类"""
    create_time = serializers.DateTimeField(label='创建时间', format='%Y-%m-%d %H:%M:%S')

    class Meta:
        model = OrderInfo
        fields = ('order_id', 'create_time')
