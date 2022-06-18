from django.urls import path

from .views import UserLogoutView, UserLoginView, RegistrationView

app_name = 'app_users'

urlpatterns = [
    path('logout', UserLogoutView.as_view(), name='logout'),
    path('login', UserLoginView.as_view(), name='login'),
    path('register', RegistrationView.as_view(), name='register')
]
