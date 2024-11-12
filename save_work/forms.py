from django import forms

from .models import Teacher, Subject


class SaveWorkForm(forms.Form):
    """
    Class for handling the form to save work with dynamic choices for teachers and specific widgets for fields.

    :type: A ModelChoiceField for selecting a subject from the available subjects.
    :teacher: A ChoiceField for selecting a teacher with choices populated dynamically during initialization.
    :work: A FileField for uploading the work file.

    Methods:
        __init__(*args, **kwargs): Initializes the form and dynamically loads the teachers for the 'teacher' ChoiceField.
    """
    type = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    teacher = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    work = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(SaveWorkForm, self).__init__(*args, **kwargs)
        self.fields['teacher'].choices = [(teacher.id, str(teacher)) for teacher in Teacher.objects.all()]
