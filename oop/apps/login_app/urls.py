from . import views
from django.conf.urls import url, include


urlpatterns = [
    url(r'^$', views.index),
    url(r'^main_login$', views.main_login),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success$', views.success),
    url(r'^logout$', views.logout),
]
