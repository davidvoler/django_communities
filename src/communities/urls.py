from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required, permission_required
from communities import views
from django.views.generic.base import TemplateView

urlpatterns = patterns('',
    url(r'^$', views.CommunityList.as_view()),
    url(r'^create/$', login_required(views.CreateCommunity.as_view())),
    url(r'^s/(?P<slug>[\w_\-]+)/$', views.CommunityView.as_view()),
    url(r'^edit/(?P<slug>[\w_\-]+)/$', views.UpdateCommunity.as_view()),
    url(r'^change_lang/$', views.set_language),
    #url(r'^change_lang/$', views.ChangeLangView.as_view()),
    url(r'^change_lang_form/$', TemplateView.as_view(template_name="communities/change_language.html")),
    url(r'^member/(?P<pk>[\w_\-]+)/$',views.CommunityMember.as_view()),
    url(r'^member/edit/(?P<pk>[\w_\-]+)/$',views.EditCommunityMember.as_view()),
)
