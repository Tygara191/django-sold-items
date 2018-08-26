from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.main_listing, name="sold_items_listing"),
    url(r'^details/(?P<slug>[-\w]+)/$', views.details, name="sold_items_details"),
]