from django.conf.urls import include, url

from meiduo_admin.views.statistical import StatisticalTotalCountView, StatisticalDayIncrementView
from meiduo_admin.views.users import AuthorizationView

urlpatterns = [
    url(r'^authorizations/$', AuthorizationView().as_view()),
    url(r'^statistical/total_count/$', StatisticalTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', StatisticalDayIncrementView.as_view()),
]