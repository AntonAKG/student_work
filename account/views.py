import os
import zipfile

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View

from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView

from save_work.models import Student, Teacher, StudentWork
from .forms import LoginForm, RegisterForm, UserProfileForm


class LoginClassView(LoginView):
    """
        LoginClassView is a class-based view for handling user login.

        It inherits from Django's LoginView and customizes the context data and
        success URL for a successful login.

        Methods:
            get_context_data: Adds custom data to the context of the login page.
            get_success_url: Defines the URL to redirect to upon a successful login.

        Attributes:
            authentication_form: Specifies the form class to use for authentication.
    """
    LoginView.authentication_form = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Login'

        return context

    def get_success_url(self):
        return reverse('profile')


class RegisterView(CreateView):
    """
        RegisterView handles user registration by using a form to create a new user, authenticating, and logging them in.

        Attributes:
            form_class: Specifies the form to be used for registration.
            template_name: Path to the template used for rendering the registration form.
            success_url: URL to redirect to upon successful registration.

        Methods:
            form_valid(self, form):
                Processes the valid form data, authenticates the user, and logs them in.
    """
    form_class = RegisterForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")
        user = authenticate(self.request, username=username, password=password)

        if user:
            login(self.request, user)

        return response


class ProfileView(LoginRequiredMixin, TemplateView):
    """
        Class to display and handle the user profile page.

        ProfileView extends LoginRequiredMixin to ensure only logged-in users can access this view,
        and TemplateView to render the profile template.

        Attributes:
        -----------
        template_name : str
            The template to be rendered for the profile view.
    """
    template_name = "account/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        student = getattr(user, 'student', None)
        if student:
            works = StudentWork.objects.filter(student=student)
        else:
            works = []

        def get_user_type(user_id):
            if Student.objects.filter(student_id=user_id).exists():
                return "Student"
            elif Teacher.objects.filter(teacher_id=user_id).exists():
                return "Teacher"
            else:
                return "Unknown"

        context["title"] = "Profile"
        context["form"] = UserProfileForm(instance=self.request.user)
        context["role"] = get_user_type(self.request.user.id)
        context['work'] = works

        return context

    def post(self, request, *args, **kwargs):
        form = UserProfileForm(request.POST, instance=self.request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return self.render_to_response(self.get_context_data(form=form))

class DownloadWorksView(LoginRequiredMixin, View):
    """
    DownloadWorksView is a class-based view that allows authenticated students to download their works in a ZIP file.

    Methods
    -------
    get(request, *args, **kwargs)
        Handles the GET request to generate and serve a ZIP file containing the student's works.

        Parameters
        ----------
        request : HttpRequest
            The GET request from the client.
        *args : tuple
            Additional positional arguments.
        **kwargs : dict
            Additional keyword arguments.

        Returns
        -------
        HttpResponse
            An HTTP response with a ZIP file containing the student's works. If the student is not found, it returns a 404 response.
    """
    def get(self, request, *args, **kwargs):
        user = request.user
        student = getattr(user, 'student', None)

        if not student:
            return HttpResponse("Student works not found.", status=404)

        zip_filename = f"{user.first_name} {user.last_name}_works.zip"
        zip_path = os.path.join(settings.MEDIA_ROOT, zip_filename)
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            works = StudentWork.objects.filter(student=student)
            for work in works:
                work_path = work.work.path
                zip_file.write(work_path, os.path.basename(work_path))

        with open(zip_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            return response

