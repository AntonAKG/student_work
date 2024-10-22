from django.urls import path

from .views import TeacherView


urlpatterns = [
    path('', TeacherView.as_view(), name='teacher_panel'),
]