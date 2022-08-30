from django import forms

from cars import models


class CarForm(forms.ModelForm):
    class Meta:
        model = models.Car
        exclude = ('owner',)


class RentalPeriodForm(forms.ModelForm):
    class Meta:
        model = models.RentalPeriod
        exclude = ('driver',)
