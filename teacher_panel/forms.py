from django import forms
from save_work.models import Student, Group
from django.contrib.auth import get_user_model

User = get_user_model()

class CreateUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Пароль")

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        labels = {
            'username': "Ім'я користувача",
            'email': "Email",
            'first_name': "Ім'я",
            'last_name': "Прізвище",
        }


class AssignStudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['group', 'age']
        labels = {
            'group': "Група",
            'age': "Вік",
        }
