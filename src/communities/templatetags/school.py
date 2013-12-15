from django import template
from django.utils.translation import ugettext as _
from communities.models import Language

register = template.Library()

@register.filter
def card_perms(card,user):
    return card.permissions(user)
card_perms.is_safe = True
