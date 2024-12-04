from django.urls import path

from .views import HomeView, ContactView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('contact/', HomeView.as_view(), name='contact'),
    path('about/', HomeView.as_view(), name='about'),

]