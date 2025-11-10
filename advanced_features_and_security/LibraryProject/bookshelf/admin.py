from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser


# Task 0 Step 4: Integrate the Custom User Model into Admin
# Custom ModelAdmin class that includes configurations for the additional fields
@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """Custom admin configuration for CustomUser model"""
    # Fields to display in the user list
    list_display = ('email', 'username', 'date_of_birth', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Fieldsets for user editing
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'date_of_birth', 'profile_photo')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fieldsets for user creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'date_of_birth', 'profile_photo'),
        }),
    )
    
    # Search and ordering
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('email',)
    
    # Make email the username field
    filter_horizontal = ('groups', 'user_permissions')

