from django.http.response import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import redirect_to_login
from django.utils.text import slugify
from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404


from communities.models import Community,Member
from communities.forms import CommunityForm,MemberForm
from communities.models.user_profile import get_user_profile
from hdi.base_views import CrumbsMixin
from lessons.models import Lesson
from communities.community_base_views import CommunityContentPermissionMixin


class CommunityList(CommunityContentPermissionMixin,ListView):
    required_permission = 'view_community_list'
    community_perm=True
    crumbs=[{'link':'/','title':_('Home')},
            {'link':'/communities/','title':_('Communities')},
            ]
    title=_('Communitys')
    model = Community

class CreateCommunity(CommunityContentPermissionMixin,CreateView):
    required_permission = 'create_community'
    title='Create Community'
    crumbs=[{'link':'/','title':_('Home')},
            {'link':'/communities/','title':_('Communities')},
            {'link':'/communities/create/','title':_('Create Community')}
            ]
    template_name = "communities/create.html"
    form_class = CommunityForm
    model = Community
    community_perm=True
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        #create this user as community Admin
        
        #form.instance.site=get_current_site(self.request)
        results = super(CreateCommunity, self).form_valid(form)
        member,created=Member.objects.get_or_create(community=form.instance,
                                            user=self.request.user,
                                            member_type='admin',
                                            accepted=True)
        member.save()
        return results
    
class UpdateCommunity(CommunityContentPermissionMixin,UpdateView):
    required_permission = 'edit_community'
    
    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg, None)
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        if slug:
            self.community=get_object_or_404(Community,slug=slug)
        elif pk:
            self.community=get_object_or_404(Community,pk=pk)
        else:
            raise AttributeError("Expecting pk or slug in update community view")
        return self.community
    def get_contnent_perm_obj(self):
        return self.get_object()
        #return self.community
    
    def get_view_info(self):
        self.title= " %s " % (self.community.name)
        
        self.crumbs=[{'link':'/','title':_('Home')},
            {'link':'/communities/','title':_('Communities')},
            {'link':'/communities/s/%s/'%self.community.slug,'title':self.community.name},
            {'link':'','title':_('Edit')}
            ]
    template_name = "communities/create.html"
    form_class = CommunityForm
    model = Community

class CommunityView(CommunityContentPermissionMixin,DetailView):
    context_object_name = 'community'
    template_name = "communities/community.html"
    model = Community
    
    def get_view_info(self):
        join=self.request.GET.get('join','')
        set_active=self.request.GET.get('set_active','')
        community=self.get_object()
        #TODO: check if user can join or not:
        #if join requires authorisation - add this kind of filed
        if join:
            profile=get_user_profile(self.request)
            notification=profile.set_community(self.request,community)
            self.more.append(('notification',notification))
        elif set_active:
            profile=get_user_profile(self.request)
            notification=profile.set_community(self.request,community)
            self.more.append(('notification',notification))
        self.title=community.name
        self.more.append(('is_member',community.is_member(self.request.user)))
        self.crumbs=[{'link':'/','title':_('Home')},
            {'link':'/communities/','title':_('Communities')},
            {'link':'/communities/s/%s/'%community.slug,'title':community.name},
            ]

class SetActiveCommunity(CommunityContentPermissionMixin,RedirectView):
    context_object_name = 'community'
    template_name = "communities/community.html"
    model = Community
    def get_view_info(self):
        community=self.get_object()
        
        self.title=community.name
        self.more.append(('is_member',community.is_member(self.request.user)))
    
from django.utils.translation import check_for_language
from django.utils import translation
def set_language(request):
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = HttpResponseRedirect(next)
    lang_id=request.GET.get('lang_id','')
    exp_lang_id=request.GET.get('exp_lang_id','')
    profile=get_user_profile(request)
    profile.set_langs(request,lang_id,exp_lang_id)
    if exp_lang_id and check_for_language(exp_lang_id):
        translation.activate(exp_lang_id)
        p=1
        if hasattr(request, 'session'):
            q=2
            request.session['django_language'] = exp_lang_id
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, exp_lang_id)
    #baba=bub
    return response


class ChangeLangView(RedirectView):
    permanent = False
    def get_redirect_url(self):
        lang_id=self.request.GET.get('lang_id','')
        exp_lang_id=self.request.GET.get('exp_lang_id','')
        profile=get_user_profile(self.request)
        profile.set_langs(self.request,lang_id,exp_lang_id)
        #if self.request.META['HTTP_REFERER']:
        if exp_lang_id and check_for_language(exp_lang_id):
            if hasattr(self.request, 'session'):
                self.request.session['django_language'] = exp_lang_id
        try:
            return self.request.META['HTTP_REFERER']
        except:
            return '/'
        

class ChangeLangFormView(RedirectView):

    permanent = False
    def get_redirect_url(self):
        lang_id=self.request.GET.get('lang_id','')
        exp_lang_id=self.request.GET.get('exp_lang_id','')
        profile=get_user_profile(self.request)
        profile.set_langs(self.request,lang_id,exp_lang_id)
        #if self.request.META['HTTP_REFERER']:
        try:
            return self.request.META['HTTP_REFERER']
        except:
            return '/'



class CommunityMember(CommunityContentPermissionMixin,DetailView):
    required_permission = 'view_community_members'
    object_name='member'
    model=Member
    template_name = "communities/member.html"
    def get_contnent_perm_obj(self):
        member=self.get_object()
        return member.community
    def get_view_info(self):
        self.title=_('member page')
        member=self.get_object()
        self.crumbs=[{'link':'/','title':_('Home')},
            {'link':'/communities/','title':_('Communities')},
            {'link':'/communities/s/%s/'%member.community.slug,'title':member.community.name},
            {'link':'','title':member.user.username},
            ]

class EditCommunityMember(CommunityContentPermissionMixin,UpdateView):
    required_permission = 'edit_community_members'
    object_name='member'
    model=Member
    template_name = "form.html"
    form_class=MemberForm
    def get_contnent_perm_obj(self):
        member=self.get_object()
        return member.community
    def get_view_info(self):
        self.title=_('Edit Member')
        member=self.get_object()
        self.crumbs=[{'link':'/','title':_('Home')},
            {'link':'/communities/','title':_('Communities')},
            {'link':'/communities/s/%s/'%member.community.slug,'title':member.community.name},
            {'link':'/communities/member/%d/'%member.pk,'title':member.user.username},
            {'link':'','title':_('Edit Member')},
            ]


create_community = permission_required('auth.change_user')(CreateCommunity.as_view())