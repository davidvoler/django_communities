from django.db import models
from django.contrib.auth.models import User
from communities.models import Community


class CommunityRelation(models.Model):
    community1 = models.ForeignKey(Community)
    community2 = models.ForeignKey(Community)
    accepted=models.BooleanField()
    accepted_by=models.ForeignKey(User)
    #Permissions
    class Meta:
        app_label = 'communities'