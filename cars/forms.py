from django import forms
from django.db.models import Q

from cars import models


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        exclude = ('owner',)


class RentalPeriodForm(forms.ModelForm):
    class Meta:
        model = models.RentalPeriod
        exclude = ('driver',)

    def is_valid(self):
        excluded_cars = models.RentalPeriod.objects.filter(
            Q(start_date__range=(self.instance['start_date'],
                                 self.instance['end_date'])) |
            Q(end_date__range=(self.instance['start_date'],
                               self.instance['end_date']))
        ).values_list('car_id')
        if self.instance['car'] in excluded_cars:
            return False
        return super().is_valid()
