from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^recognize/this/$', views.simple_upload, name='simple_upload'),
    url(r'^$', views.index, name='index'),
]