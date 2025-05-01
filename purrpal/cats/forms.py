from django import forms
from django.contrib.auth.models import User
from .models import UserProfile


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    gender = forms.ChoiceField(choices=[("male", "Male"), ("female", "Female"), ("other", "Other")])
    role = forms.ChoiceField(choices=[('regular', 'Regular'), ('admin', 'Admin')])


    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            # Create or get existing UserProfile
            profile, created = UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'gender': self.cleaned_data['gender'],
                    'role': 'admin'
                }
            )
        return user

