from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext as _

User = get_user_model()


class Student(models.Model):
    student = models.OneToOneField(User, on_delete=models.CASCADE)
    group = models.CharField(max_length=10)
    age = models.IntegerField()

    def __str__(self):
        return f'{self.student} {self.group} {self.age}'


class Subject(models.Model):
    subject = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.subject}'

class Teacher(models.Model):
    teacher = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher}'

class StudentWork(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    work = models.FileField(upload_to='work')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
