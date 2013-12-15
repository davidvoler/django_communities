from django.db import models
from django.contrib.sites.models import Site
from communities.models import Community
 
class SiteCommunity(models.Model):
    site = models.OneToOneField(Site)
    school =  models.ForeignKey(Community)
    class Meta:
        app_label = 'schools'
    def __unicode__(self):
        return "%s - %s"%( self.site.name,self.school.name)
