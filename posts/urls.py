from posts.views import CreatePosts, ImagenCreateView, BasicPlusVersionCreateView,ImagenDeleteView, PostsDetails, PostsView, PostsListView, PuntosTemplateView

__author__ = 'vdjke'
from django.conf.urls import include, url

urlpatterns = [
    url(r'^create/$', CreatePosts.as_view(), name="create-posts"),
    url(r'^previsualizar/$', PostsDetails.as_view(), name='previsualizar_posts'),
    url(r'^ver/(?P<pk>\d+)/(?P<slug>[-\w\d]+)/$', PostsView.as_view(), name='ver-posts'),
    url(r'^puntuar/$', PuntosTemplateView.as_view(), name='puntuar-posts'),
    url(r'^basic/plus/$', BasicPlusVersionCreateView.as_view(), name='upload-basic-plus'),
    url(r'^new/$', ImagenCreateView.as_view(), name='upload-new'),
    url(r'^delete/(?P<pk>\d+)$', ImagenDeleteView.as_view(), name='upload-delete'),
]
