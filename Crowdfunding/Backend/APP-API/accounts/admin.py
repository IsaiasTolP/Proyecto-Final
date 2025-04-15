from django.contrib import admin
from .models import Profile, FounderProfile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(FounderProfile)
class FounderProfileAdmin(admin.ModelAdmin):
    pass
