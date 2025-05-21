from django.contrib import admin
from .models import Contribution
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeNumericListFilter, TextFilter, RangeDateTimeFilter
from django.core.validators import EMPTY_VALUES
from django.utils.translation import gettext_lazy
from simple_history.admin import SimpleHistoryAdmin

class AmountFilter(RangeNumericListFilter):
    parameter_name = 'amount'
    title = 'Dinero aportado'
    
class UsernameFilter(TextFilter):
    title = gettext_lazy('Nombre de usuario')
    parameter_name = 'contributor'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(contributor__username__icontains=self.value())
        
        return queryset

class ProjectNameFilter(TextFilter):
    title = gettext_lazy('Nombre de proyecto')
    parameter_name = 'project__name'

    def queryset(self, request, queryset):
        if self.value() not in EMPTY_VALUES:
            return queryset.filter(project__name__icontains=self.value())
    
        return queryset

@admin.register(Contribution)
class ContributionAdmin(SimpleHistoryAdmin, ModelAdmin):
    list_filter_submit = True
    list_filter = [
        AmountFilter,
        UsernameFilter,
        ProjectNameFilter,
        ('date', RangeDateTimeFilter),
    ]
