from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.Form):
    age = forms.IntegerField(min_value=0, max_value=150, required=False)
    gender = forms.ChoiceField(
        choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')],
        required=False
    )
    height_cm = forms.FloatField(required=False, help_text='Height in centimeters')
    weight_kg = forms.FloatField(required=False, help_text='Weight in kilograms')
