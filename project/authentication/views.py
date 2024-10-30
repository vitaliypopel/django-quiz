from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.views.decorators.http import require_http_methods

from .forms import RegistrationForm


@method_decorator(require_http_methods(['GET', 'POST']), name='dispatch')
class RegistrationView(FormView):
    form_class = RegistrationForm
    template_name = 'registration/registration.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
