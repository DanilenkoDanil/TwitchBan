from django.contrib import admin
from base.models import Chanel, TelegramAccount


@admin.register(TelegramAccount)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id')


@admin.register(Chanel)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'link', 'spectators', 'subscribers', 'ban', 'check_date', 'ban_date', 'county')
    search_fields = ('title', 'link', 'ban')
