from django.conf.urls import patterns, url
from communities import views

urlpatterns = patterns('',
    url(r'^$', views.CommunityList.as_view()),
    url(r'^s/(?P<slug>[\w_\-]+)/$', views.CommunityView.as_view()),
    url(r'^edit/(?P<slug>[\w_\-]+)/$', views.UpdateCommunity.as_view()),
    url(r'^member/(?P<pk>[\w_\-]+)/$',views.CommunityMember.as_view()),
    url(r'^member/edit/(?P<pk>[\w_\-]+)/$',views.EditCommunityMember.as_view()),
)
