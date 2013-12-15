from django.http import HttpResponseForbidden
from django.conf import settings
from django.contrib.auth.views import redirect_to_login


from communitys.models import Community
from communitys.models.user_profile import get_user_profile
from communitys.models.community_content import CommunityContent

class CommunityMixin(object):
    crumbs=[]
    #title='No Title Set'
    page_title=''
    more=[]
    profile=None
    community_perm=False
    def get_view_info(self):
        return None
    def get_context_data(self, **kwargs):
        data = super(CommunityMixin, self).get_context_data(**kwargs)
        self.get_view_info()
        if hasattr(self,'menu'):
            data['menu']=self.menu
        if hasattr(self,'page_cid'):
            data['page_cid']=self.page_cid
        else:
            data['page_cid']=self.__class__.__name__
        try:
            data['crumbs'] = self.crumbs
            data['title']=self.title
            if self.page_title:
                data['page_title']=self.page_title
            else:
                data['page_title']=self.title
        except:
            pass    
        try:
            data['edit_stage']=self.edit_stage
        except:
            pass
        try:    
            data['content_perms']=self.content_perms
        except:
            pass
        for m in self.more:
            data[m[0]]=m[1]
            #data.append( [m[0]]=m[1])
        #if 'lesson' in data:
        #    print 'after more'
        #    print data['lesson']
        #import pprint
        #pp = pprint.PrettyPrinter(indent=4)
        #pp.pprint(data)
        return data
    def get_content_perm_obj(self):
        if hasattr(self,'get_object'):
            return self.get_object()
        else:
            return self.profile
    def get_perm_obj(self,request):
        self.profile=get_user_profile(request)
        if self.community_perm:
            return self.profile
            
        obj=self.get_content_perm_obj()
        if issubclass(obj.__class__, CommunityContent):
            return obj
        elif obj.__class__==Community:
            return obj
        else:
            return self.profile
    def dispatch(self, request, *args, **kwargs):
        self.perm_obj=self.get_perm_obj(request)
        self.content_perms=self.perm_obj.content_perms(request.user)
        if hasattr(self, 'required_permission'):
            if not self.required_permission in self.content_perms:
                if not request.user.is_authenticated():
                    return redirect_to_login(request.build_absolute_uri())
                if settings.DEBUG:
                    return HttpResponseForbidden("403 %s" % self.required_permission)
                return HttpResponseForbidden("403 Unauthorized")                
        return super(CommunityContentPermissionMixin, self).dispatch(request, *args, **kwargs)
        #return response