from django.contrib import admin
from .models import Process
# Register your models here.

@admin.register(Process)
class User_profileAdmin(admin.ModelAdmin):
    list_display = ('actor', 'process_type', 'progress', 'created_at')
    ordering = ('process_type', 'progress', 'created_at')

