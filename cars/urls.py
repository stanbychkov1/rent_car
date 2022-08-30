from django.urls import path, include
from django.views import generic

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('rent/', views.CarsView.as_view(), name='rent'),
    path('success/', views.SuccessView.as_view(), name='success'),
    path('add_car/', views.AddCarView.as_view(), name='add_car'),
    ]