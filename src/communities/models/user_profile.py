from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import ugettext_lazy as _

from communities.models.user_language import UserLanguage
from communities.models.language import Language
from communities.models import Community,Member
from bookmarks.models import Bookmark
"""
Changes: Unite edit and learn languages
make lang exp_lang a property
get community list

"""
class UserProfilePermMixin(object):
    def content_perms(self,user):
        return self.community.perms(user)
    def has_permission(self,perm):
        return self.community.has_permission(self.user,perm)
    def perms(self):
        return self.community.perms(self.user)
    def view_content(self):
        return 'view' in self.perms() 
    def add_content(self):
        return 'create' in self.perms() 
    def edit_contnet(self):
        return 'edit' in self.perms() 
    def comment(self):
        return 'comment' in self.perms() 
    def ask_question(self):
        return 'ask_question' in self.perms() 
    def get_langs_title(self):
        pass
    def communities(self):
        return self.community.list_communities(self.user)
    def lesson_count(self):
        from lessons.models import Lesson
        return Lesson.objects.filter(community=self.community,
                                     lang=self.lang,
                                     exp_lang=self.exp_lang,
                                     published=True).count()
    def course_count(self):
        from courses.models import Course
        return Course.objects.filter(community=self.community,
                                     lang=self.lang,
                                     exp_lang=self.exp_lang,
                                     published=True).count()
    def exercise_count(self):
        from exercises.models import Exercise
        return Exercise.objects.filter(community=self.community,
                                     lang=self.lang,
                                     exp_lang=self.exp_lang,
                                     published=True).count()
    def bookmarks(self):
        return Bookmark.get_bookmark(self.user)
        

class UserProfile(models.Model,UserProfilePermMixin):
    user = models.ForeignKey(User, unique=True,null=True)
    community =  models.ForeignKey(Community,null=True)
    theme = models.CharField(max_length=100, blank=True, null=True)
    lang =  models.ForeignKey(Language, null=True,blank=True,related_name='p_lang')
    exp_lang =  models.ForeignKey(Language, null=True,blank=True,related_name='p_exp_lang')
    edit_lang =  models.ForeignKey(Language, null=True,blank=True,related_name='p_edit_lang')
    edit_exp_lang =  models.ForeignKey(Language, null=True,blank=True,related_name='p_edit_exp_lang')
    edit_level =  models.IntegerField (null=True,blank=True,default=0)
    spam = models.IntegerField(default=0)
    #state = models.CharField(max_length=30,default='student')
        
    def is_spam(self):
        return False
    def __unicode__(self):
        return self.user.username
    class Meta:
        app_label = 'communities'
    def set_community_langs(self,member):
        scooll_langs=self.community.langs.all()
        if not self.lang in scooll_langs:
            member.lang=scooll_langs[0]
        else:
            member.lang=self.lang
        community_exp_langs=self.community.exp_langs.all()
        if not self.exp_lang in community_exp_langs:
            member.exp_lang=community_exp_langs[0]
        else:
            member.exp_lang=self.exp_lang
        member.save()
    def member(self):
        member,created=Member.objects.get_or_create(community=self.community,user=self.user)
        if created:
            self.set_community_langs(member)
            member.save()
        return member
    def get_lang(self):
        try:
            return self.member().lang
        except:
            return None
    def get_exp_lang(self):
        try:
            return self.member().exp_lang
        except:
            return None
    def get_community(self,request):
        if not self.community:
            self.community= Community.get_default(request)
            #add as a member
            self.save()
        return self.community
    def set_community(self,request,community):
        self.community= community
        notification=''
        member,created=Member.objects.get_or_create(community=community,
                                                    user=self.user)
        if created:
            if community.has_permission(self.user,'join_community_auto_accept',):
                member.accepted=True
                notification=_('You have successfully joined %s')%community.name
            else:
                notification=_('Your request to joined %s as been registered, waiting for authorization')%community.name
                
            member.save()
        else:
            notification=_('%s is your active community now')%community.name
        self.set_community_langs(member)
        self.save()
        return notification
        
    def set_edit_langs(self,edit_lang,edit_exp_lang,level=0):
        #TBD:Add edit langs
        self.edit_lang=edit_lang
        self.edit_exp_lang=edit_exp_lang
        self.edit_level=level
        self.save()
    def set_langs(self,request,lang_id,exp_lang_id):
        #TBD:Add edit langs
        member=self.member()
        if lang_id:
            try:
                lang=Language.objects.get(pk=lang_id)
                self.lang=lang
                self.save()
                member.lang=lang
                member.save()
            except:
                pass
        if exp_lang_id:
            try:
                exp_lang=Language.objects.get(pk=exp_lang_id)
                self.exp_lang=exp_lang
                self.save()
                member.exp_lang=exp_lang
                member.save()
            except:
                pass
    def mode(self):
        return 'student'
    def modes(self):
        return ['student','author','admin']
    """
    TODO: enable different state for user so he sees different menus
    def get_states(self):
        member_type=self.community.
    """
class AnonProfile(UserProfilePermMixin):
    def __init__(self,user,request=None):
        self.community=None
        self.user=user
        self.state='student'
        if request:
            try:
                self.lang=request.session['lang']
            except:
                self.lang=None
            try:
                self.exp_lang=request.session['exp_lang']           
            except:
                self.exp_lang=None
        else:
            self.lang=None
            self.exp_lang=None
    def set_langs(self,request,lang_id,exp_lang_id):
        if lang_id:
            try:
                lang=Language.objects.get(pk=lang_id)
                self.lang=lang
                request.session['lang']=lang
            except:
                pass
        if exp_lang_id:
            try:
                exp_lang=Language.objects.get(pk=exp_lang_id)
                self.exp_lang=exp_lang
                request.session['exp_lang']=exp_lang
            except:
                pass

    def get_lang(self):
        return self.lang
    def get_exp_lang(self):
        return self.exp_lang
    def test(self):
        return "TEST"
    def get_langs(self,learning):
        return []
    def get_l_langs(self):
        return []
    def get_exp_langs(self):
        return []
    def get_order_langs(self,learning):
        return Language.objects.all()
    def get_l_order_langs(self):
        return self.get_order_langs(True)
    def get_d_order_langs(self):
        return self.get_order_langs(False)
    def get_l_my_langs(self):
        return []
    def get_d_my_langs(self):
        return []
    def get_l_other_langs(self):
        return Language.objects.all()
    def get_d_other_langs(self):
        return Language.objects.all()
    def set_lang(self,lang,learning=True):
        #problem we need a request here.
        pass
    def is_spam(self):
        return False
    def get_community(self,request):
        if not self.community:
            try:
                community_id=request.session['community_id']
                self.community=Community.objects.get(pk=community_id)
            except:
                self.community=Community.get_default(request)
                request.session['community_id']= self.community.pk
        else:
            return self.community
        return self.community
        """
        try:
            community_id=request.session['community_id']
        except:
            community_id=''
        if community_id:
            try:
                self.community=Community.objects.get(pk=community_id)
            except:
                self.community=Community.get_default(request)
        else:
            self.community=Community.get_default(request)
        if self.community:
            request.session['community_id']= self.community.pk
        return self.community
        """
    def set_community(self,request,community):
        request.session['community_id']= community.pk
        self.community=community
        return _('%s is your active community now')%community.name

    def set_edit_langs(self,edit_lang,edit_exp_lang):
        return None
    def get_langs_title(self):
        return "Anonimus langs"

def get_or_create_user_profile(u,request=None):
    if u.is_active:
        profile,created=UserProfile.objects.get_or_create(user=u)
        if created:
            profile.save()
        return profile
    else:
        return AnonProfile(u,request)

def get_user_profile(request):
    profile=get_or_create_user_profile(request.user,request)
    profile.get_community(request)
    return profile
#User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.profile = property(lambda u: get_or_create_user_profile(u))        
AnonymousUser.profile = property(lambda u: get_or_create_user_profile(u))