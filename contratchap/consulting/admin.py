from django.contrib import admin
from .models import Consulting

@admin.register(Consulting)
class ConsultingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number', 'meet_day', 'consulting_hour', 'status', 'created_at')
    list_filter = ('status', 'meet_day', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number', 'title', 'description')
    ordering = ('-created_at',)
