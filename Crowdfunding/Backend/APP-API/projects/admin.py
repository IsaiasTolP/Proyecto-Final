from django.contrib import admin
from .models import Project, ProjectCategory, ProjectImage, ProjectSponsorship
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import TextFilter, RangeDateTimeFilter, RangeDateFilter, RelatedDropdownFilter
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy
from simple_history.admin import SimpleHistoryAdmin

class OwnerUsernameFilter(TextFilter):
    title = gettext_lazy('Nombre de usuario')
    parameter_name = 'owner'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(owner__username__icontains=self.value())
        
        return queryset

class UsernameFilter(TextFilter):
    title = gettext_lazy('Nombre de usuario')
    parameter_name = 'user'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(user__username__icontains=self.value())
        
        return queryset

class ProjectNameFilter(TextFilter):
    title = gettext_lazy('Nombre de proyecto')
    parameter_name = 'name'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(name__icontains=self.value())
    
        return queryset

class ProjectOnSponsorshipNameFilter(TextFilter):
    title = gettext_lazy('Nombre de proyecto')
    parameter_name = 'project__name'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(project__name__icontains=self.value())
    
        return queryset


@admin.register(Project)
class ProjectAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_filter_submit = True
    list_filter = [
        OwnerUsernameFilter,
        ProjectNameFilter,
        ('category', RelatedDropdownFilter),
        ('start_date', RangeDateFilter),
    ]

@admin.register(ProjectImage)
class ProjectImageAdmin(SimpleHistoryAdmin, ModelAdmin):
    pass

@admin.register(ProjectCategory)
class ProjectCategoryAdmin(SimpleHistoryAdmin, ModelAdmin):
    pass

@admin.register(ProjectSponsorship)
class ProjectSponsorshipAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_filter_submit = True
    list_filter = [
        UsernameFilter,
        ProjectOnSponsorshipNameFilter,
        ('date', RangeDateTimeFilter),
    ]