from django import forms

from .models import Teacher, Subject


class SaveWorkForm(forms.Form):
    type = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    # Оновлюємо віджет на Select
    teacher = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    work = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    # Перевизначаємо метод ініціалізації для динамічного завантаження вчителів
    def __init__(self, *args, **kwargs):
        super(SaveWorkForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].choices = [(teacher.id, str(teacher)) for teacher in Teacher.objects.all()]
