from django.contrib import admin
from django.contrib.auth.models import Group
from django.utils.html import format_html

from .models import Client, EquipmentCatalog, EquipmentCategory, GeneralCatalog


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        'user_id',
        'full_name',
        'contact_phone',
        'client_status',
        'telegram_profile',
        'created_at']
    readonly_fields = [
        'user_id',
        'username',
        'full_name',
        'contact_phone',
        'client_status',
        'preferences',
        'created_at']

    ordering = ['-created_at']
    search_fields = ['full_name', 'contact_phone', 'client_status']
    list_filter = ['client_status']

    def telegram_profile(self, obj):
        if obj.username:
            telegram_url = f'https://t.me/{obj.username}'
            return format_html('<a href="{}" target="_blank">@{}</a>', telegram_url, obj.username)
        return None

    telegram_profile.short_description = 'Telegram Profile'


@admin.register(EquipmentCatalog)
class EquipmentCatalogAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['title']


@admin.register(GeneralCatalog)
class GeneralCatalogAdmin(admin.ModelAdmin):
    list_display = ['pdf_file']


admin.site.site_header = 'RedEnCo'
admin.site.site_title = 'RedEnCoBot'

admin.site.unregister(Group)
