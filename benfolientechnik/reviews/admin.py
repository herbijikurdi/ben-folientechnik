from django.contrib import admin
from .models import Review, Gallery

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'rating', 'created_at')
    list_filter = ('service', 'rating')
    search_fields = ('name', 'email', 'comment')

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('order', 'created_at')