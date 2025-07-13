from django.contrib import admin
from .models import User, UserToken, UserProfile, UserPermission, UserSession, UserActivity, UserNotification


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'last_name', 'mail', 'type', 'is_active', 'is_confirmed', 'created_at']
    list_filter = ['type', 'is_active', 'is_deleted', 'is_confirmed', 'created_at']
    search_fields = ['name', 'last_name', 'mail', 'google_id', 'code']
    readonly_fields = ['code', 'created_at', 'updated_at', 'confirmed_at', 'deleted_at', 'log', 'version']
    ordering = ['name', 'last_name']


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'ip_address', 'created_at', 'expires_at', 'revoked_at']
    list_filter = ['created_at', 'expires_at', 'revoked_at']
    search_fields = ['user_id', 'token', 'ip_address']
    readonly_fields = ['id', 'created_at']
    ordering = ['-created_at']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone', 'is_active', 'franchise', 'created_at']
    list_filter = ['role', 'is_active', 'franchise', 'created_at']
    search_fields = ['user__username', 'user__first_name', 'user__last_name', 'phone']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['user__username']


@admin.register(UserPermission)
class UserPermissionAdmin(admin.ModelAdmin):
    list_display = ['permission_name', 'user', 'is_active', 'created_by', 'created_at']
    list_filter = ['permission_name', 'is_active', 'created_at']
    search_fields = ['permission_name', 'description', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['permission_name']


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'session_key', 'ip_address', 'login_time', 'is_active', 'franchise']
    list_filter = ['is_active', 'franchise', 'login_time']
    search_fields = ['session_key', 'ip_address', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-login_time']


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'ip_address', 'activity_date', 'franchise']
    list_filter = ['activity_type', 'franchise', 'activity_date']
    search_fields = ['description', 'ip_address', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-activity_date']


@admin.register(UserNotification)
class UserNotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notification_type', 'is_read', 'created_at']
    list_filter = ['notification_type', 'is_read', 'created_at']
    search_fields = ['title', 'message', 'user__username']
    readonly_fields = ['created_at']
    ordering = ['-created_at']
