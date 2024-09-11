from django.urls import path

from .views import SaveWorkView

urlpatterns = [
    path('', SaveWorkView.as_view(), name='save_work'),
]