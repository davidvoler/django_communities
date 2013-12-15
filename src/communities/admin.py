from django.contrib import admin
from communities.models import Community,Member,Language,SiteCommunity,UserProfile

class CommunityAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    exclude=('slug',)
class LanguageAdmin(admin.ModelAdmin):
    search_fields = ('name',)
#class ExplanationLanguageAdmin(admin.ModelAdmin):
#    search_fields = ('name',)


admin.site.register(Community, CommunityAdmin)
admin.site.register(Member)
admin.site.register(Language, LanguageAdmin)
#admin.site.register(ExplanationLanguage, ExplanationLanguageAdmin)
admin.site.register(SiteCommunity)
admin.site.register(UserProfile)
