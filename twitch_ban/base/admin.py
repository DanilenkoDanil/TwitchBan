from django.contrib import admin
from django.utils.html import format_html
from base.models import Chanel, TelegramAccount


@admin.register(TelegramAccount)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('name', 'telegram_id')


@admin.register(Chanel)
class SettingAdmin(admin.ModelAdmin):
    list_display = ('title', 'show_link', 'spectators', 'subscribers', 'ban', 'check_date', 'ban_date', 'county')
    search_fields = ('title', 'link', 'ban')

    def show_link(self, obj):
        return format_html("<a href='{url}' target='_blank'>{url}</a>", url=obj.link)
