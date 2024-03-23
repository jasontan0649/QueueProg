# queue_app/admin.py
from django.contrib import admin
from .models import QueueNumber

@admin.register(QueueNumber)
class QueueNumberAdmin(admin.ModelAdmin):
    list_display = ('number', 'message', 'created_at')  # Add other fields you want to display
    ordering = ('-created_at',)  # Order by created_at in descending order
    search_fields = ('number', 'message')  # Add search functionality for these fields
