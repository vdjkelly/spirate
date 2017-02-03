from django.conf.urls import include, url
from usuarios.views import FollowView, UnFollowView, LoginUserFormView, salir

urlpatterns = [
    url(r'^social/', include('social.apps.django_app.urls',  namespace="social")),
    url(r'^follows/$', FollowView.as_view(), name='seguir-usuario'),
    url(r'^unfollow/$', UnFollowView.as_view(), name='dejarde-seguir'),
    url(r'^login/$', LoginUserFormView.as_view(), name='acount-login'),
    url(r'^salir/$', view=salir, name='acount-logout')
]
