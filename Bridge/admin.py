from django.contrib import admin
from Bridge.models import Campaign


class CampaignAdmin(admin.ModelAdmin):
    list_display = ('campaign_id', 'campaign_name', 'campaign_level', 'app_id')

admin.site.register(Campaign, CampaignAdmin)
