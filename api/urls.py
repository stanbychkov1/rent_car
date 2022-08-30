from django.urls import include, path

from . import views

urlpatterns = [
    path('signup/', views.SignUpApiView.as_view(), name='sign_up_api'),
    path('token/', views.CustomObtainAuthToken.as_view(), name='token'),
    path('user_cars/', views.UserCarsApiView.as_view(), name='user_cars'),
    path('all_users/', views.AllUsersApiView.as_view(), name='all_users'),
    path('me/', views.MeApiView.as_view(), name='me'),
]
