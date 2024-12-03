from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext as _

class Group(models.Model):
    group_name = models.CharField(max_length=100)
    group_slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")

    def __str__(self):
        return self.group_name


class Student(models.Model):
    student = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    slug = models.SlugField(
        max_length=200, unique=True, blank=True, null=True, verbose_name="URL"
    )
    age = models.IntegerField()

    def __str__(self):
        return f'{self.student} {self.group.group_name} {self.age}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.student.username.split('@')[0])  # Використовуємо частину email до "@"
            original_slug = self.slug
            for i in range(1, 1000):
                if not Student.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f"{original_slug}-{i}"

        super().save(*args, **kwargs)


class Subject(models.Model):
    subject = models.CharField(max_length=50)

    def __str__(self):
        return f'{self.subject}'


class Teacher(models.Model):
    teacher = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.teacher}'


class StudentWork(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    type = models.ForeignKey(Subject, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    work = models.FileField(upload_to='work')
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    def __str__(self):
        return f'{self.student} {self.type} {self.teacher} {self.group} {self.work} {self.date_joined}'
