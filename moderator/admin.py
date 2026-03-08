from django.contrib import admin
from django.utils import timezone
from .models import ModRole


@admin.register(ModRole)
class ModRoleAdmin(admin.ModelAdmin):
    list_display   = ('session_token', 'status', 'kindness_at_grant', 'actions_today', 'total_actions', 'granted_at')
    list_filter    = ('status',)
    ordering       = ('-kindness_at_grant',)
    actions        = ['approve_mods', 'revoke_mods']

    def approve_mods(self, request, queryset):
        
        for mod in queryset.filter(status='candidate'):
            mod.approve()
        self.message_user(request, f"Approved {queryset.count()} moderators.")
    approve_mods.short_description = "Approve selected candidates"

    def revoke_mods(self, request, queryset):
    
        for mod in queryset.filter(status='active'):
            mod.revoke()
        self.message_user(request, f"Revoked {queryset.count()} moderators.")
    revoke_mods.short_description = "Revoke selected moderators"