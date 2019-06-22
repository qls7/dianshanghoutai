import os

from meiduo_admin.serializers.skus import SKUSSerializer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
import django

django.setup()

from meiduo_admin.views.skus import SKUImagesViewSet, SKUSimpleView, SKUSViewSet

from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter

from meiduo_admin.views import users
from meiduo_admin.views.channels import GoodsChannelViewSet, GoodsChannelTypesView, GoodsChannelCategoriesView
from meiduo_admin.views.statistical import *
from meiduo_admin.views.users import AuthorizationView

urlpatterns = [
    # 登录页面
    url(r'^authorizations/$', AuthorizationView().as_view()),
    # 统计页面
    url(r'^statistical/total_count/$', StatisticalTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', StatisticalDayIncrementView.as_view()),
    url(r'^statistical/day_active/$', StatisticalDayActiveView.as_view()),
    url(r'^statistical/day_orders/$', StatisticalDayOrdersView.as_view()),
    url(r'^statistical/month_increment/$', StatisticalMonthIncrementView.as_view()),
    url(r'^statistical/goods_day_views/$', StatisticalGoodsDayView.as_view()),
    # 用户管理
    url(r'^users/$', users.UsersView.as_view()),
    # 获取频道组
    url(r'^goods/channel_types/$', GoodsChannelTypesView.as_view()),
    # 获取一级分类数据
    url(r'^goods/categories/$', GoodsChannelCategoriesView.as_view()),
    # 获取简单skus
    url(r'^skus/simple/$', SKUSimpleView.as_view())
]

# 频道管理
router = DefaultRouter()
router.register('goods/channels', GoodsChannelViewSet)
urlpatterns += router.urls
# 图片管理
router = DefaultRouter()
router.register(r'skus/images', SKUImagesViewSet)
urlpatterns += router.urls
# sku管理
router = DefaultRouter()
router.register(r'skus', SKUSViewSet)
urlpatterns += router.urls

if __name__ == '__main__':
    print(router.urls)
