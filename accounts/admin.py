from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age', 'gender', 'weight_kg', 'height_cm')
    list_filter = ('gender', 'created_at')
    search_fields = ('user__username', 'user__email')
