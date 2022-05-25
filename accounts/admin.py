from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import Institution, Donation


# Register your models here.


class AccountAdmin(UserAdmin):
    """Define admin model for custom User model with no username field."""
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

def is_taken(model_admin, request, query_set):
    query_set.update(is_taken=True)


is_taken.short_description = 'Dar został odebrany !'


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    actions = [is_taken, ]
    list_display = ('quantity', 'institution', 'phone_number', 'pick_up_date', 'is_taken')

admin.site.register(get_user_model(), AccountAdmin)

admin.site.register(Institution)