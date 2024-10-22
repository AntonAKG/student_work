from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from save_work.models import StudentWork, Group


@method_decorator(login_required, name='dispatch')
class TeacherView(UserPassesTestMixin, TemplateView):
    template_name = 'teacher_panel/main_teacher_panel.html'

    def test_func(self):
        return self.request.user.is_staff or self.request.user.is_superuser

    def handle_no_permission(self):
        return self.redirect_to_login(reverse_lazy('login'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Отримуємо ID групи з параметрів GET
        group_id = self.request.GET.get('group_id')

        if group_id:
            # Якщо вибрано групу, фільтруємо роботи за нею
            context['student_work'] = StudentWork.objects.filter(group_id=group_id)
        else:
            # Якщо група не вибрана, відображаємо всі роботи
            context['student_work'] = StudentWork.objects.all()

        # Передаємо всі групи для фільтрації
        context['groups'] = Group.objects.all()
        print(Group.objects.all())

        return context
