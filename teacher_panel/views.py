import os
import os.path
import zipfile

import tempfile
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.cache import cache
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, DetailView, FormView
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from .forms import CreateUserForm, AssignStudentForm
from save_work.models import Group, Subject
from save_work.models import StudentWork, Student


class TeacherBaseView(UserPassesTestMixin):
    """
    class TeacherBaseView(UserPassesTestMixin):
    """

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser # Перевірка чи користувач є вчителем

    def handle_no_permission(self):
        # Redirect to the login page if the user lacks permission
        return redirect_to_login(self.request.get_full_path(), login_url=reverse_lazy('login'))

    def get_common_context_data(self, **kwargs):
        context = cache.get('common_context_data')
        if not context:
            context = {
                'groups': Group.objects.all(),
                'subjects': Subject.objects.all()
            }
            cache.set('common_context_data', context, timeout=60 * 15)  # Кешуємо на 15 хвилин
        return context


class TeacherView(TeacherBaseView, TemplateView):
    """
        TeacherView(TeacherBaseView, TemplateView) class

        A view that handles the display of the main teacher panel. Inherits from TeacherBaseView and TemplateView.

        Attributes:
        -----------
        template_name : str
            The template name for the view.

        Methods:
        --------
        get_context_data(self, **kwargs)
            Retrieves and returns context data for rendering the template. Filters student work based on query parameters
            such as search_query, group_id, and subject_id.
    """
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
    """
    StudentTeacherPanel is a view that inherits from TeacherBaseView and TemplateView. It is responsible for displaying the student teacher panel interface, which lists all students.

    Attributes:
        template_name (str): Path to the HTML template for rendering the student teacher panel interface.

    Methods:
        get_context_data(self, **kwargs):
            Adds a list of all students to the context data.

            Parameters:
                **kwargs: Arbitrary keyword arguments.

            Returns:
                dict: Context data including a list of all students.
    """
    template_name = 'teacher_panel/student_teacher_panel.html'

    def get_context_data(self, **kwargs):
        context = super().get_common_context_data(**kwargs)
        search_query = self.request.GET.get('search', '')
        group_id = self.request.GET.get('group_id')

        # Get unique groups
        student_groups = Student.objects.values_list('group__id', 'group__group_name').distinct()

        # Remove duplicates manually (if needed)
        unique_groups = {group_id: group_name for group_id, group_name in student_groups}
        group_options = [{'id': gid, 'group_name': gname} for gid, gname in unique_groups.items()]

        # Filter students by selected group, if group_id is provided
        students = Student.objects.all()
        if group_id:
            students = students.filter(group_id=group_id)

        if search_query:
            students = students.filter(
                student__first_name__istartswith=search_query
            ) | students.filter(
                student__last_name__istartswith=search_query
            )

        context['student_filter'] = students
        context['group_options'] = group_options
        context['search_query'] = search_query

        return context


class TeacherPersonalView(TeacherBaseView, DetailView):
    """
    TeacherPersonalView class, inheriting from TeacherBaseView and DetailView, provides a detailed view of a specific student’s account, including their related work, which can be filtered and sorted based on the request parameters.

    Attributes:
        template_name (str): Specifies the template to render the student's account.
        model (type): The model associated with the view, set to Student.
        slug_field (str): The field used to look up the student; specified as 'slug'.
        slug_url_kwarg (str): The URL keyword argument representing the slug; set to 'slug'.

    Methods:
        get_context_data(**kwargs):
            Extends the context data for the view by including the student information and their associated work, filtered and sorted based on query parameters from the request.

            Parameters:
                kwargs: Arbitrary keyword arguments.

            Returns:
                dict: The updated context dictionary including the student object, filtered and sorted student work, and the current sort order.
    """
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



class CreateStudentView(FormView):
    template_name = 'teacher_panel/student_create_account.html'
    success_url = reverse_lazy('student_teacher_panel')

    def get(self, request, *args, **kwargs):
        user_form = CreateUserForm()
        student_form = AssignStudentForm()
        return render(request, self.template_name, {
            'user_form': user_form,
            'student_form': student_form,
        })

    def post(self, request, *args, **kwargs):
        user_form = CreateUserForm(request.POST)
        student_form = AssignStudentForm(request.POST)

        if user_form.is_valid() and student_form.is_valid():
            # Створення користувача
            user = user_form.save(commit=False)
            user.set_password(user_form.cleaned_data['password'])
            user.save()

            # Прив'язка до студента
            student = student_form.save(commit=False)
            student.student = user
            student.save()

            return redirect(self.success_url)

        # Повернення форм у разі помилок
        return render(request, self.template_name, {
            'user_form': user_form,
            'student_form': student_form,
        })

    def get_student_form(self):
        """
        Ініціалізація студентської форми з фільтрацією.
        """
        form = self.student_form_class()
        User = get_user_model()  # Динамічно отримуємо кастомну модель користувача
        student_group, created = Group.objects.get_or_create(group_name='student')  # Використовуйте get_or_create
        students = User.objects.filter(groups=student_group)
        form.fields['student'].queryset = students  # Поле називається 'student', а не 'user'
        return form

    def assign_student_group(self, user):
        """
        Додаємо користувача до групи "student".
        """
        student_group, created = Group.objects.get_or_create(name='student')
        student_group.user_set.add(user)


class DownloadStudentWorksZipView(View):
    """
        A Django view that handles the process of fetching a student's works from the database,
        compressing the works into a ZIP file, and serving the ZIP file as a downloadable response.

        get(request, slug)
            Handles GET requests to download a ZIP file containing a student's works.

            Parameters:
                request: The HTTP request object.
                slug: The unique identifier for the student.

            Raises:
                Http404: If no works are found for the student.

            Returns:
                HttpResponse: A response object that serves the ZIP file for download.
    """

    def get(self, request, slug):
        student = get_object_or_404(Student, slug=slug)
        works = StudentWork.objects.filter(student=student)

        if not works:
            raise Http404("No works found for this student")

        with tempfile.TemporaryDirectory() as temp_dir:
            zip_filename = f"{student.student.first_name}_{student.student.last_name}_works.zip"
            zip_path = os.path.join(temp_dir, zip_filename)

            with zipfile.ZipFile(zip_path, 'w') as zip_file:
                for work in works:
                    file_path = work.work.path
                    if os.path.exists(file_path):
                        zip_file.write(file_path, os.path.basename(file_path))

            with open(zip_path, 'rb') as zip_file:
                response = HttpResponse(zip_file.read(), content_type='application/zip')
                response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'
            return response
