from django.contrib import admin

from users import models


class MyUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'first_name', 'last_name', 'username',
                    'language', 'is_staff', 'is_active', 'is_superuser')
    search_fields = ('pk', 'email', 'first_name', 'last_name', 'username',
                     'language', 'is_staff', 'is_active', 'is_superuser')
    empty_value_display = '-empty-'


admin.site.register(models.MyUser, MyUserAdmin)
