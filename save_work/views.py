from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect
from django.utils import timezone
from .forms import SaveWorkForm
from .models import StudentWork, Student, Subject, Teacher


class SaveWorkView(View):
    """
        A Django View for handling the display and submission of the SaveWorkForm.

        This class-based view manages two primary functions:
        1. Displaying the form to the user via a GET request.
        2. Handling the submission of the form and saving the work data via a POST request.

        Attributes:
            template_name (str): The template that will be used to render the form.

        Methods:
            get(request, *args, **kwargs):
                Handles the GET request to display the form.
                Renders the form and a title within the provided template.

            post(request, *args, **kwargs):
                Handles the POST request to process form data.
                If the form is valid, saves a new StudentWork object with the provided data.
                Redirects the user to the /save_work/ URL upon successful save.
                If the form is not valid, re-renders the form with validation errors.
    """
    template_name = 'save_work/save_work.html'

    # Обробка GET-запиту (відображення форми)
    def get(self, request, *args, **kwargs):
        form = SaveWorkForm()
        return render(request, self.template_name, {'form': form, 'title': 'Save Work'})

    # Обробка POST-запиту (збереження даних)
    def post(self, request, *args, **kwargs):
        form = SaveWorkForm(request.POST, request.FILES)
        if form.is_valid():
            # Отримуємо студента із поточного користувача
            student = Student.objects.get(student=request.user)
            group_ = student.group

            # Отримуємо об'єкти із форми
            type = form.cleaned_data['type']  # Це вже об'єкт Subject
            work = form.cleaned_data['work']  # Це файл
            teacher_id = form.cleaned_data['teacher']  # Це вже об'єкт Teacher
            teacher = Teacher.objects.get(id=teacher_id)

            # Створюємо новий об'єкт StudentWork і зберігаємо його
            student_work = StudentWork(
                student=student,
                type=type,
                teacher=teacher,  # Використовуємо екземпляр Teacher, а не ID
                work=work,
                group=group_,
                date_joined=timezone.now()
            )
            student_work.save()

            # Перенаправляємо після успішного збереження
            return HttpResponseRedirect("/save_work/")

        # Якщо форма невалідна, виводимо її з помилками
        return render(request, self.template_name, {'form': form, 'title': 'Save Work'})
