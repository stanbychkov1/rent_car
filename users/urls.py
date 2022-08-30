from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from . import views
from .forms import UserAuthForm

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('login/', LoginView.as_view(authentication_form=UserAuthForm),
         name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(),
         name='profile_update'),
]
