import os
import zipfile

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView

from save_work.models import StudentWork, Group, Student, Subject


@method_decorator(login_required, name='dispatch')
class TeacherView(UserPassesTestMixin, TemplateView):
    template_name = 'teacher_panel/main_teacher_panel.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return self.redirect_to_login(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        search_query = self.request.GET.get('search', '')

        group_id = self.request.GET.get('group_id')

        if group_id:
            student_work = StudentWork.objects.filter(group_id=group_id)
        else:
            student_work = StudentWork.objects.all()

        if search_query:
            student_work = student_work.filter(
                student__student__first_name__icontains=search_query
            ) | student_work.filter(
                student__student__last_name__icontains=search_query
            )

        context['student_work'] = student_work
        context['groups'] = Group.objects.all()
        context['search_query'] = search_query

        return context


@method_decorator(login_required, name='dispatch')
class TeacherPersonalView(UserPassesTestMixin, DetailView):
    template_name = 'teacher_panel/student_account.html'
    model = Student
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return self.redirect_to_login(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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

        context['save_work_student'] = work_queryset
        context["subjects"] = Subject.objects.all()
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

        # Create the temporary directory if it doesn't exist
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)

        # Create the ZIP file path
        zip_filename = f"{student.student.first_name}_{student.student.last_name}_works.zip"
        zip_path = os.path.join(temp_dir, zip_filename)

        # Create the ZIP file and add each student's work
        with zipfile.ZipFile(zip_path, 'w') as zip_file:
            for work in works:
                file_path = work.work.path
                zip_file.write(file_path, os.path.basename(file_path))

        # Serve the ZIP file as a downloadable response
        with open(zip_path, 'rb') as zip_file:
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

        # Delete the ZIP file after serving the response
        os.remove(zip_path)

        return response
