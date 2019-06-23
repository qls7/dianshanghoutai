from rest_framework.decorators import action
from rest_framework.generics import RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from meiduo_admin.serializers.orders import OrdersViewSerializer, OrdersDetailViewSerializer, OrdersUpdateSerializer
from orders.models import OrderInfo


# 对于使用的资源是一样的视图接口可以使用同一视图集, 根据请求的action选择不同的序列化器类
# GET /meiduo_admin/orders/?keyword=<搜索内容>&page=<页码>&pagesize=<页容量>
class OrdersViewSet(ReadOnlyModelViewSet):
    """订单管理视图接口"""
    permission_classes = [IsAdminUser]
    queryset = OrderInfo.objects.all()
    serializer_class = OrdersViewSerializer

    # PUT /meiduo_admin/orders/(?P<pk>\d+)/status/
    # 自定义请求方式其实就是UpdateAPIView
    # 自定义的请求方式如果要添加路由需要加上装饰器
    @action(methods=['put'], detail=True)
    def status(self, request, pk):
        """自定义修改状态请求方式"""
        # 先校验pk
        # 再或取data的值进行校验
        # 保存data
        # return response()
        # try:
        #     order = OrderInfo.objects.get(pk=pk)
        # except:
        #     raise Exception('订单编号错误')
        order = self.get_object()
        data = self.request.data
        serializer = OrdersUpdateSerializer(instance=order, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def get_serializer_class(self):
        """根据action确定使用的序列化器类"""
        if self.action == 'list':
            return OrdersViewSerializer
        else:
            return OrdersDetailViewSerializer

    def get_queryset(self):
        """根据关键字确定视图集"""
        keyword = self.request.query_params.get('keyword')
        if keyword:
            return OrderInfo.objects.filter(skus__sku__name__contains=keyword)
        else:
            return OrderInfo.objects.all()
