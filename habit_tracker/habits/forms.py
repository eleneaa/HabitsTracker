from .models import Habit
from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['title', 'description', 'is_completed_today', 'attachment']


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
