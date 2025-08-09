from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'rating', 'created_at')
    list_filter = ('service', 'rating')
    search_fields = ('name', 'email', 'comment')