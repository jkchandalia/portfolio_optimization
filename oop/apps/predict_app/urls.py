from . import views
from django.conf.urls import url, include

urlpatterns = [
    url('^$', views.call_model.as_view()),
]