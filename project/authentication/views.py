from django.views.generic import FormView, View
from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy
from django.shortcuts import redirect, reverse

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_GET, require_http_methods

from .forms import RegistrationForm


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'authentication/registration.html'
    success_url = reverse_lazy('authentication:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('quiz:dashboard')

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(
            request=self.request,
            username=cd['username'],
            password=cd['password'],
        )

        if not user:
            form.add_error(
                'password',
                'Invalid username or password',
            )
            return super().form_invalid(form)

        login(self.request, user)
        return super().form_valid(form)


@method_decorator([login_required, require_GET], name='dispatch')
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('quiz:home'))
