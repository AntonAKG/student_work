from django.urls import path, include

from .views import LoginClassView, RegisterView, ProfileView, DownloadWorksView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', LoginClassView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', ProfileView.as_view(), name='profile'),
    path('download_works/', DownloadWorksView.as_view(), name='download_student_works'),

]