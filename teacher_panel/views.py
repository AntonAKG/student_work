import os
import os.path
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView

from save_work.models import Group, Subject
from save_work.models import StudentWork, Student


class TeacherBaseView(UserPassesTestMixin):
    """
    Base view for teacher-related views, handling permission checks
    and setting up common context data.
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        # Redirect to the login page if the user lacks permission
        return redirect_to_login(self.request.get_full_path(), login_url=reverse_lazy('login'))

    def get_common_context_data(self, **kwargs):
        """Add common context data for groups and subjects."""
        context = {}
        context['groups'] = Group.objects.all()
        context['subjects'] = Subject.objects.all()
        return context


class TeacherView(TeacherBaseView, TemplateView):
    template_name = 'teacher_panel/main_teacher_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_common_context_data(**kwargs)

        search_query = self.request.GET.get('search', '')
        group_id = self.request.GET.get('group_id')
        subject_id = self.request.GET.get('subject')

        student_work = StudentWork.objects.all()

        if group_id:
            student_work = student_work.filter(group_id=group_id)

        if subject_id:
            student_work = student_work.filter(type_id=subject_id)

        if search_query:
            student_work = student_work.filter(
                student__student__first_name__icontains=search_query
            ) | student_work.filter(
                student__student__last_name__icontains=search_query
            )

        context['student_work'] = student_work
        context['search_query'] = search_query

        return context


class StudentTeacherPanel(TeacherBaseView, TemplateView):
    template_name = 'teacher_panel/student_teacher_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_common_context_data(**kwargs)

        context['students'] = Student.objects.all()

        return context

class TeacherPersonalView(TeacherBaseView, DetailView):
    template_name = 'teacher_panel/student_account.html'
    model = Student
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_common_context_data(**kwargs)
        student = get_object_or_404(Student, slug=self.kwargs['slug'])

        # Get filter parameters from the request
        subject_id = self.request.GET.get('subject_id')
        sort_order = self.request.GET.get('sort_order', 'newest')  # Default to newest

        # Apply filtering by subject
        work_queryset = StudentWork.objects.filter(student=student)
        if subject_id:
            work_queryset = work_queryset.filter(type__id=subject_id)

        # Apply sorting by date
        if sort_order == 'oldest':
            work_queryset = work_queryset.order_by('date_joined')
        else:
            work_queryset = work_queryset.order_by('-date_joined')

        context['student'] = student
        context['save_work_student'] = work_queryset
        context["current_sort_order"] = sort_order

        return context


class DownloadStudentWorksZipView(View):
    def get(self, request, slug):
        # Fetch the student and their works
        student = get_object_or_404(Student, slug=slug)
        works = StudentWork.objects.filter(student=student)

        # If no works are found, raise a 404 error
        if not works:
            raise Http404("No works found for this student")

        # Create a temporary directory for ZIP files
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Set up the ZIP file path
        zip_filename = f"{student.student.first_name}_{student.student.last_name}_works.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        # Create the ZIP file
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for work in works:
                file_path = work.work.path
                try:
                    if os.path.exists(file_path):
                        zip_file.write(file_path, os.path.basename(file_path))
                    else:
                        print(f"File {file_path} does not exist and will be skipped.")
                except Exception as e:
                    print(f"An error occurred: {e}")

        # Serve the ZIP file as a downloadable response
        with open(zip_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        # Clean up by deleting the ZIP file after serving it
        os.remove(zip_path)

        return response
