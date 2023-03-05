from django.contrib import admin
from base.models import Chanel


@admin.register(Chanel)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'spectators', 'ban', 'check_date', 'ban_date', 'county')
    search_fields = ('title', 'link', 'ban')
