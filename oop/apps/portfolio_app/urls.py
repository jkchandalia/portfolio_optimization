from django.conf.urls import url
#from django.contrib import admin
from . import views
urlpatterns = [
#    url(r'^admin/', admin.site.urls),
    url(r'^index$', views.index),
    url(r'^main$', views.main),
    url(r'^validate_option$', views.validate_option),
    url(r'^remove_option$', views.remove_option),
    url(r'^options$', views.update_portfolio),
    url(r'^instructions$', views.instructions),
    url(r'^analysis$', views.analysis),
    url(r'^update_margin_avail$', views.update_margin_avail),
    url(r'^plot_options$', views.plot_options, name="plot"),
    url(r'^send_slack_msg$', views.send_slack_msg),
    url(r'^update_market_data$', views.update_market_data),
    url(r'^simulate_shock$', views.simulate_shock),
    url(r'^toggle_summary$', views.toggle_summary),
]
