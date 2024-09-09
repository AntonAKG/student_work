from audioop import reverse

from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth import login

from .forms import LoginForm, RegisterForm


class LoginClassView(LoginView):
    LoginView.authentication_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Login'

        return context

    def get_success_url(self):
        return reverse('profile')

class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)

        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, email=email, password=password)

        if user:
            login(self.request, user)

        return response

class ProfileView(TemplateView):
    template_name = 'account/profile.html'