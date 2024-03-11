from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from .models import UserProfile, UserTagPreference, UserFavorite

# Register UserProfile model inline with User model
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'

# Custom UserAdmin to display UserProfile inline
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)

    # Custom method to get the is_moderator value from UserProfile
    def is_moderator(self, obj):
        try:
            user_profile = UserProfile.objects.get(user=obj)
            return user_profile.is_moderator
        except UserProfile.DoesNotExist:
            return False

    is_moderator.boolean = True  
    is_moderator.short_description = 'Is Moderator'  

    list_display = ('username', 'email', 'is_staff', 'is_moderator')

# Unregister the default User model
admin.site.unregister(User)

# Register the User model with the custom UserAdmin
@admin.action(description='Make selected users moderators')
def make_moderators(modeladmin, request, queryset):
    moderator_group = Group.objects.get(name='Moderators')
    for user in queryset:
        user_profile, created = UserProfile.objects.get_or_create(user=user)
        user_profile.is_moderator = True
        user_profile.save()
        user.groups.add(moderator_group)

@admin.action(description='Remove moderator status from selected users')
def remove_moderators(modeladmin, request, queryset):
    moderator_group = Group.objects.get(name='Moderators')
    for user in queryset:
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_moderator = False
        user_profile.save()
        user.groups.remove(moderator_group)

admin.site.register(User, CustomUserAdmin)
admin.site.register(UserProfile)
admin.site.register(UserTagPreference)
admin.site.register(UserFavorite)