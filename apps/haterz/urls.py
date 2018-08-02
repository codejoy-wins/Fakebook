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

    url(r'^', views.odell),
]
