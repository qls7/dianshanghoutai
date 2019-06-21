from django.conf.urls import include, url

from meiduo_admin.views import users
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
    url(r'^users/$', users.UsersView.as_view())
]