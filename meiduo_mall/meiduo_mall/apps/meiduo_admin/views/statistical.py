from datetime import timedelta
from django.utils import timezone
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.statistical import StatisticalGoodsDayViewSerializer
from orders.models import OrderInfo
from users.models import User


# GET /meiduo_admin/statistical/goods_day_views/
class StatisticalGoodsDayView(ListAPIView):
    """获取日分类商品访问量"""
    permission_classes = [IsAdminUser]
    date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    queryset = GoodsVisitCount.objects.filter(create_time__gte=date)
    serializer_class = StatisticalGoodsDayViewSerializer

    pagination_class = None

# GET /meiduo_admin/statistical/month_increment/
class StatisticalMonthIncrementView(APIView):
    """获取30天内新增用户的数量"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        start_date = date - timedelta(days=29)
        next_date = start_date + timedelta(days=1)
        date_list = []
        for i in range(30):
            count = User.objects.filter(date_joined__gte=start_date, date_joined__lt=next_date).count()
            date_list.append({
                'count': count,
                'date': start_date.date(),
            })
            start_date += timedelta(days=1)
            next_date += timedelta(days=1)

        return Response(date_list)


# GET /meiduo_admin/statistical/day_orders/
class StatisticalDayOrdersView(APIView):
    """获取日下单用户量"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        # count = OrderInfo.objects.filter(create_time__gt=date).count()
        # 用用户表去关联查询订单表,把查出来的信息进行去重处理,获取到当前下单的用户量
        count = User.objects.filter(orders__create_time__gt=date).distinct().count()
        return Response({'count': count, 'date': date.date()})


# GET /meiduo_admin/statistical/day_active/
class StatisticalDayActiveView(APIView):
    """获取网站日活跃用户"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        date = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        count = User.objects.filter(last_login__gt=date, is_staff=False).count()
        return Response({'count': count, 'date': date.date()})


# GET /meiduo_admin/statistical/day_increment/
class StatisticalDayIncrementView(APIView):
    """获取网站日新增用户"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        date = timezone.now().replace(hour=0, microsecond=0, minute=0, second=0)
        count = User.objects.filter(date_joined__gt=date, is_staff=False).count()
        return Response({'count': count, 'date': date.date()})


# GET /meiduo_admin/statistical/total_count/
class StatisticalTotalCountView(APIView):
    """获取网站总用户数量"""
    # 获取总用户数量
    # 进行返回
    permission_classes = [IsAdminUser]

    def get(self, request):
        count = User.objects.all().count()
        date = timezone.now().date()
        data = {
            'count': count,
            'date': date,
        }
        return Response(data)
