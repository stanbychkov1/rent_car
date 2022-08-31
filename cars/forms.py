import datetime

from django import forms
from django.core.exceptions import ValidationError
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

    def clean(self):
        super(RentalPeriodForm, self).clean()
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')

        if start_date < datetime.date.today() or end_date < start_date:
            self._errors['start_date'] = self.error_class([
                'Дата начала не может быть меньше сегодня'
            ])
            self._errors['end_date'] = self.error_class([
                'Дата конца не может быть меньше даты начала или сегодня'
            ])
        return self.cleaned_data

    def is_valid(self):
        start_date = self.data['start_date']
        end_date = self.data['end_date']
        car = self.data['car']

        excluded_cars = models.RentalPeriod.objects.filter(
            Q(start_date__range=(start_date, end_date)) |
            Q(end_date__range=(start_date, end_date))
        )
        if car in excluded_cars:
            return False
        return super().is_valid()
