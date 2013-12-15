from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.sites.models import get_current_site


class Community(models.Model):
    name = models.CharField(max_length=25, verbose_name=_("Name"),unique=True)
    moto = models.CharField(max_length=200, verbose_name=_("Moto"),null=True, default='',
                            help_text='A short sentence about the community')
    description=models.TextField( verbose_name=_("Description"),null=True,blank=True,
                            help_text='Describe your community, Description will be shown on home page')
    slug=models.SlugField(max_length=200, verbose_name=_("Slug"),unique=True)
    created_by = models.ForeignKey(User)
    site=models.ForeignKey(Site,null=True,blank=True,editable=False)
    permission=models.ForeignKey(PermGroup,verbose_name=_('Permission'),null=True)
    theme = models.CharField(max_length=100, default='cerulean', 
                             choices=THEMES,
                            null=True)
    logo = models.FileField(upload_to='community_logo', verbose_name=_("Community Logo"), 
                            blank=True, null=True)
    langs=models.ManyToManyField(Language,related_name='s_langs')
    exp_langs=models.ManyToManyField(Language,related_name='s_exp_langs')
    published=models.BooleanField(default=False)
    blocked=models.BooleanField(default=False)
    class Meta:
        app_label = 'communities'
    def get_absolute_url(self):
        return '/communities/s/%s/'%self.slug
    def __unicode__(self):
        return self.name
    def save(self, *args, **kwargs):
        self.slug = uuslug(self.name, instance=self)
        super(Community, self).save(*args, **kwargs)
    @staticmethod
    def get_default(request):
        from communities.models.site_community import SiteCommunity
        try:
            request_site=request.META['HTTP_HOST']
            site=Site.objects.get(domain=request_site)
        except:
            site=get_current_site(request)
        try:
            site_community=SiteCommunity.objects.get(site=site)
            return site_community.community
        except:
            return None
    def member_type(self,user):
        user_type=''
        if user.is_active:
            user_type='active'
            try:
                member = self.member_set.get(user=user,accepted=True,blocked=False)      
                user_type=member.member_type
            except:
                pass
        else:
            user_type='anon'
        return user_type     
    def is_member(self,user):
        try:
            member = self.member_set.get(user=user,accepted=True,blocked=False)
            return True
        except:
            return False
    def perms(self,user,own=False):
        return self.permission.get_perm(self.member_type(user),own)
    def has_permission(self,user,perm,own=False):
        if perm in self.perms(user,own):
            return True
        else:
            return False
    def all_permissions(self,own):
        return []
    def content_perms(self,user):
        own=False
        if self.created_by==user:
            own=True
        return self.perms(user,own)
    def list_communities(self,user):
        #TODO: show only communities for users current language
        
        return Community.objects.all().exclude(pk=self.pk)
