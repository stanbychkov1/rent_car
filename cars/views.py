import datetime

from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin

from cars import forms, models
from rent_car import settings


class IndexView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'index.html'


class SuccessView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'misc/success.html'

    def get_context_data(self, **kwargs):
        referer = self.request.META.get('HTTP_REFERER')
        context = super(SuccessView, self).get_context_data(**kwargs)
        if 'add_car' in referer:
            context['success'] = 'Автомобиль добавлен'
            return context
        elif 'rent' in referer:
            context['success'] = 'Автомобиль забронирован'
            return context
        elif 'profile/update' in referer:
            context['success'] = 'Данные профиля обновлены'
            return context
        return context


class CarsView(LoginRequiredMixin, generic.FormView, generic.ListView):
    template_name = 'cars.html'
    form_class = forms.RentalPeriodForm
    success_url = reverse_lazy('success')

    def get(self, request, *args, **kwargs):
        date_format = '%Y-%m-%d'
        start_date = datetime.datetime.strptime(
            self.request.GET.get('start_date'), date_format).date()
        end_date = datetime.datetime.strptime(
            self.request.GET.get('end_date'), date_format).date()
        if start_date < datetime.date.today() >= end_date \
                or start_date > end_date:
            return redirect(to='index')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        excluded_cars = models.RentalPeriod.objects.filter(
            Q(start_date__range=(start_date, end_date)) |
            Q(end_date__range=(start_date, end_date))
        ).values_list('car_id')
        cars = models.Car.objects.exclude(id__in=excluded_cars)
        return cars

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.instance.driver = self.request.user
            form.save()
            return self.form_valid(form)
        return self.form_invalid(form)


class AddCarView(LoginRequiredMixin, generic.FormView):
    template_name = 'add_car.html'
    form_class = forms.CarForm
    success_url = reverse_lazy('success')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        form.save()
        theme = 'Автомобиль добавлен'
        message = f' Автомобиль {form.instance.title} добавлен в систему.'
        send_mail(theme, message, settings.EMAIL_HOST_USER,
                  [self.request.user.email, ], fail_silently=False)
        return super().form_valid(form)
