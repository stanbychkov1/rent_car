from django.contrib import admin

from cars import models


class CarAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'prod_year', 'created_at',
                    'owner',)
    search_fields = ('pk', 'owner__first_name', 'owner__email',
                     'owner__last_name', 'prod_year',
                     'created_at',)
    empty_value_display = '-empty-'


class RentalPeriod(admin.ModelAdmin):
    list_display = ('pk', 'car', 'driver', 'start_date',
                    'end_date',)
    search_fields = ('pk', 'car__title', 'car__prod_year',
                     'car__owner__first_name', 'car__owner__last_name',
                     'car__owner__email', 'start_date', 'end_date',)
    empty_value_display = '-empty-'


admin.site.register(models.Car, CarAdmin)
admin.site.register(models.RentalPeriod, RentalPeriod)
