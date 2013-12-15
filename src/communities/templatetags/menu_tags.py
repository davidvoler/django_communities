from django.template import Library
from django.utils.safestring import mark_safe


MENU_ICONS=( ('' ,'icon-home') ,
            ('exercises','icon-pencil'),
            ('lessons','icon-file'),
            ('courses','icon-book'),
            ('practice','icon-edit'),
              )
register = Library()

@register.filter(is_safe=True)
def menu_icon(link):
    try:
        menu=link.split('/')[-2]
        print menu
        for m in MENU_ICONS:
            if menu==m[0]:
                return mark_safe(m[1])
    except:
        return 'icon-star'
    return 'icon-star'

