from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.models import Group

from .access import TECH_ADMIN, roles_for
from .models import User


class TechnicalAdminSite(admin.AdminSite):
    site_header = 'NUAM · Administración técnica'
    site_title = 'Administración NUAM'

    def has_permission(self, request):
        user = request.user
        return user.is_authenticated and user.is_active and user.is_staff and TECH_ADMIN in roles_for(user)


class AccountAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (('Corredor', {'fields': ('broker',)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (('Corredor', {'fields': ('broker',)}),)
    list_display = ('username', 'broker', 'is_active', 'is_staff')


site = TechnicalAdminSite(name='admin')
site.register(User, AccountAdmin)
site.register(Group, GroupAdmin)
