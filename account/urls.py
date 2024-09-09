from django.urls import path, include

from .views import LoginClassView, RegisterView, ProfileView

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login/', LoginClassView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', ProfileView.as_view(), name='profile'),
]