from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.main),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^edit/(?P<record_id>\d+)$', views.edit),
    url(r'^destroy/(?P<record_id>\d+)$', views.destroy),
    url(r'^hate/(?P<record_id>\d+)$', views.hate),
    url(r'^update/(?P<record_id>\d+)$', views.update),
    url(r'^wall/(?P<wall_id>\d+)$', views.wall),
    url(r'^post/(?P<wall_id>\d+)$', views.post),
    url(r'^like/(?P<post_id>\d+)$', views.like),
    url(r'^comment/(?P<post_id>\d+)$', views.comment),
    url(r'^custom$', views.custom),

    url(r'^', views.odell),
]
