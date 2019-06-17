from django.conf.urls import include, url

from meiduo_admin.views.users import AuthorizationView

urlpatterns = [
    url(r'^authorizations/$', AuthorizationView().as_view())
]