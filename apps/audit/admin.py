from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'utilisateur', 'action', 'content_type', 'object_id', 'description')
    list_filter = ('action', 'content_type', 'date')
    search_fields = ('description', 'utilisateur__username')
    date_hierarchy = 'date'
    readonly_fields = ('date', 'utilisateur', 'action', 'content_type', 'object_id', 'description')