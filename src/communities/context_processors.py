from django.conf import settings
from django.template import RequestContext
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404
from django.core import serializers
from django.contrib.auth.models import User
from communities.models import Community
from communities.models.user_profile import get_user_profile
def community(request):
    profile=get_user_profile(request)
    return {'profile':profile}
        