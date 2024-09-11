from django.contrib import admin

from .models import Student, Teacher, StudentWork, Subject


@admin.register(Student)
class UserAdmin(admin.ModelAdmin):
    list_display = ("student", "group")


@admin.register(Teacher)
class UserAdmin(admin.ModelAdmin):
    list_display = ("teacher", )


@admin.register(Subject)
class UserAdmin(admin.ModelAdmin):
    list_display = ("subject", )


@admin.register(StudentWork)
class UserAdmin(admin.ModelAdmin):
    list_display = ('student', 'teacher', 'type', 'date_joined')
