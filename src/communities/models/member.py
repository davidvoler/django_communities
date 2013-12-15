from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from communities.models.community import Community

class Member(models.Model):
    community =  models.ForeignKey(Community)
    user =  models.ForeignKey(User)
    created_date  = models.DateTimeField(auto_now_add=True,editable=False,default=None,null=True,blank=True)
    changed  = models.DateTimeField(auto_now=True,editable=False,default=None,null=True,blank=True)
    accepted =  models.BooleanField()
    blocked =  models.BooleanField()
    class Meta:
        app_label = 'communities'
    def __unicode__(self):
        return '%s - %s'%(self.user.username,self.community.name)
    def get_absolute_url(self):
        return '/communities/member/%d/'%self.pk
