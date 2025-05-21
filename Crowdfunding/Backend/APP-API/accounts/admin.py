from django.contrib import admin
from .models import Profile, FounderProfile
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import TextFilter
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy
from simple_history.admin import SimpleHistoryAdmin

class UsernameFilter(TextFilter):
    title = gettext_lazy('Nombre')
    parameter_name = 'user'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(user__username__icontains=self.value())
        
        return queryset

class LocationFilter(TextFilter):
    title = gettext_lazy('Ubicación')
    parameter_name = 'location'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(location__icontains=self.value())
        
        return queryset

@admin.register(Profile)
class ProfileAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_filter_submit = True
    list_filter = [
        UsernameFilter,
        LocationFilter
    ]


@admin.register(FounderProfile)
class FounderProfileAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_filter_submit = True
    list_filter = [
        UsernameFilter,
        LocationFilter
    ]
