from django.urls import path

from .views import TeacherView, TeacherPersonalView, DownloadStudentWorksZipView


urlpatterns = [
    path('', TeacherView.as_view(), name='teacher_panel'),
    path('personal_student/<slug:slug>', TeacherPersonalView.as_view(), name='teacher_personal'),
    path('download_student_works/<slug:slug>/', DownloadStudentWorksZipView.as_view(),
         name='download_student_works_zip'),
]