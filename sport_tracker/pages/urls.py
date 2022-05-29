from django.urls import include, re_path
from pages import views

urlpatterns = [
    re_path(r'^$', views.home_view, name='home'),
    re_path(r'^matches/$', views.show_matches, name='matches'),
    re_path(r'^matches/new/$', views.create_match, name='new_match'),
    re_path(r'^rejected/$', views.show_rejected_matches, name='rejected_matches'),
    re_path(r'^confirmations/$', views.show_confirmations, name='confirmations'),
    re_path(r'^stats/$', views.show_stats, name='stats'),
    re_path(r'^message/(?P<pk>\d+)/(?P<rej>\d+)/$', views.message_about_match, name="message_about_match"),
    re_path(r'^message/(?P<pk>\d+)/(?P<rej>\d+)/renew/$', views.renew_match, name="renew_match"),
    re_path(r'^exports/$', views.export_view, name='exports'),

]
