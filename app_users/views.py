from django.contrib.auth.views import LogoutView, LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from app_users.forms import RegistrationUserForm


class UserLogoutView(LogoutView):
    next_page = 'app_main:index'


class UserLoginView(LoginView):
    template_name = 'app_users/register_login.html'
    success_url = 'app_main:catalog'

    def get_context_data(self, **kwargs):
        context = super(UserLoginView, self).get_context_data()
        context['register_form'] = RegistrationUserForm
        return context


class RegistrationView(CreateView):
    form_class = RegistrationUserForm
    success_url = reverse_lazy('app_main:index')
