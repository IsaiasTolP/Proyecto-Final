from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone
from datetime import datetime
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin
from simple_history.admin import SimpleHistoryAdmin

User = get_user_model()

class UserAdmin(BaseUserAdmin, SimpleHistoryAdmin, ModelAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}

        total_users = User.objects.count()

        now = timezone.localtime(timezone.now())
        first_day_month = datetime(now.year, now.month, 1, tzinfo=now.tzinfo)
        users_this_month = User.objects.filter(date_joined__gte=first_day_month).count()

        extra_context['total_users'] = total_users
        extra_context['users_this_month'] = users_this_month

        return super().changelist_view(request, extra_context=extra_context)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)
