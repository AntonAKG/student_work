from django import forms
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    """
        LoginForm
        A customized authentication form to redefine widgets and their attributes.

        :param args: Variable-length argument list
        :param kwargs: Arbitrary keyword arguments
    """
    def __init__(self, *args, **kwargs):
        """
        redefined widget i change attribute widget
        :param args:
        :param kwargs:
        """
        super().__init__(*args, **kwargs)
        self.fields['username'].widget = forms.widgets.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Логін'
        })
        self.fields['username'].label = ''

        self.fields['password'].widget = forms.widgets.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Пароль'
        })
        self.fields['password'].label = ''


class RegisterForm(UserCreationForm):
    """
        RegisterForm
        ------------
        A form for registering a new user. Inherits from UserCreationForm.

        Attributes:
        -----------
        username : CharField
            A required field for the user's login name with a custom widget for display.

        password1 : CharField
            A required field for the user's password with a custom widget for display.

        password2 : CharField
            A required field for the password confirmation with a custom widget for display.

        first_name : CharField
            An optional field for the user's first name with a custom widget for display.

        last_name : CharField
            An optional field for the user's last name with a custom widget for display.

        Meta
        ----
        A nested class to specify the meta-data for the RegisterForm.

        model : User
            Specifies that this form is for creating a User model instance.

        fields : list
            Lists the fields to be included in the form.
    """
    username = forms.CharField(label='', required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Login'
    }))

    password1 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'password'
    }))

    password2 = forms.CharField(label='', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'repeat password'
    }))

    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": "Name"
    }))

    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={
        'class': 'form-control',
        "placeholder": "Surname"
    }))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name']


class UserProfileForm(UserChangeForm):
    """

        UserProfileForm

        A form for updating user profile information. This form inherits from
        the UserChangeForm and provides fields for first name, last name,
        and username. The username field is read-only.

        Attributes
        ----------
        first_name : forms.CharField
            A character field for the user's first name, rendered with a specific CSS class for styling.

        last_name : forms.CharField
            A character field for the user's last name, rendered with a specific CSS class for styling.

        username : forms.CharField
            A read-only character field for the user's username, rendered with a specific CSS class for styling.

        Meta
        ----
        model : User
            The model that this form is linked to, which is the User model.

        fields : tuple
            A tuple specifying the fields to be included in the form, which are 'first_name', 'last_name', and 'username'.

    """
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username')
