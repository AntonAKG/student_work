from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'main/home.html'

class ContactView(TemplateView):
    template_name = 'main/contact.html'

class AboutView(TemplateView):
    template_name = 'main/about.html'