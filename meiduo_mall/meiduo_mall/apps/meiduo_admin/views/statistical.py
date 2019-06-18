from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from users.models import User


# GET /meiduo_admin/statistical/day_increment/
class StatisticalDayIncrementView(APIView):
    """获取网站日新增用户"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        date = timezone.now().replace(hour=0, microsecond=0, minute=0, second=0)
        count = User.objects.filter(date_joined__gt=date, is_staff=False).count()
        return Response({'count':count, 'date': date})


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
