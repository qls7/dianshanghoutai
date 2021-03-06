import os

from meiduo_admin.views.brands import GoodsBrandsViewSet
from meiduo_admin.views.options import SpecOptionsViewSet

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
import django

django.setup()
from meiduo_admin.views.specs import GoodsSpecsViewSet
from meiduo_admin.views.permissions import PermsViewSet, PermsTypesView, PermsGroupViewSet, PermsAdminsViewSet
from meiduo_admin.views.orders import OrdersViewSet

from meiduo_admin.views.spus import SPUSSimpleView, GoodsCategorySimpleView, SPUSpecificationView, SPUSViewSet

from meiduo_admin.views.skus import SKUImagesViewSet, SKUSimpleView, SKUSViewSet

from django.conf.urls import url
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
    url(r'^skus/simple/$', SKUSimpleView.as_view()),
    # 获取简单的spus分类
    url(r'^goods/simple/$', SPUSSimpleView.as_view()),
    # 获取简单的三级分类
    url(r'^skus/categories/$', GoodsCategorySimpleView.as_view()),
    # 获取spu商品规格信息
    url(r'^goods/(?P<pk>\d+)/specs/$', SPUSpecificationView.as_view()),
    # 修改skus的接口路由
    url(r'^skus/(?P<pk>\d+)/specs/$', SKUSViewSet.as_view(
        {'put': 'update'}
    )),
    # 获取权限类型列表数据
    url(r'^permission/content_types/$', PermsTypesView.as_view()),
    # 获取简易权限数据
    url(r'^permission/simple/$', PermsGroupViewSet.as_view(
        {'get': 'simple'}
    )),
    # 获取简易用户组数据
    url(r'^permission/groups/simple/$', PermsAdminsViewSet.as_view(
        {'get': 'simple'}
    )),
    # 获取简易品牌数据
    url(r'^goods/brands/simple/$', SPUSViewSet.as_view(
        {'get': 'brands_simple'}
    )),
    # 获取商品一级分类
    url(r'goods/channel/categories/$', SPUSViewSet.as_view(
        {'get': 'channel_categories'}
    )),
    # 获取商品二三分类
    url(r'goods/channel/categories/(?P<pk>\d+)/$', SPUSViewSet.as_view(
        {'get': 'channel_categories'}
    )),
    # 获取规格列表
    url(r'goods/specs/simple/$', SpecOptionsViewSet.as_view({
        'get': 'simple'
    })),
]

# 频道管理
router = DefaultRouter()
router.register(r'goods/channels', GoodsChannelViewSet)
urlpatterns += router.urls

# 图片管理
router = DefaultRouter()
router.register(r'skus/images', SKUImagesViewSet)
urlpatterns += router.urls

# sku管理
router = DefaultRouter()
router.register(r'skus', SKUSViewSet)
urlpatterns += router.urls

# 订单管理
router = DefaultRouter()
router.register(r'orders', OrdersViewSet)
urlpatterns += router.urls

# 权限管理
router = DefaultRouter()
router.register(r'permission/perms', PermsViewSet)
urlpatterns += router.urls

# 权限组管理
router = DefaultRouter()
router.register(r'permission/groups', PermsGroupViewSet)
urlpatterns += router.urls

# 管理员用户管理
router = DefaultRouter()
router.register(r'permission/admins', PermsAdminsViewSet)
urlpatterns += router.urls

# spu管理
router = DefaultRouter()
router.register(r'goods', SPUSViewSet)
urlpatterns += router.urls

# specs管理
router = DefaultRouter()
router.register(r'goods/specs', GoodsSpecsViewSet)
urlpatterns += router.urls

# options管理
router = DefaultRouter()
router.register(r'specs/options', SpecOptionsViewSet)
urlpatterns += router.urls

# brands管理
router = DefaultRouter()
router.register(r'goods/brands', GoodsBrandsViewSet)
urlpatterns += router.urls

if __name__ == '__main__':
    print(router.urls)
