
from allauth.account.forms import SignupForm, AddEmailForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from users.models import User
from .widgets import CustomClearableFileInput

class CustomSignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs.update({
            'type': 'password',
            'name': 'password',
            'id': 'id_password',
            'placeholder': 'Password',
        
        })

    first_name = forms.CharField(max_length=250, label='First name', help_text='First Name', widget=forms.TextInput(
            attrs={"placeholder":("First Name")}
        ))
    
    last_name = forms.CharField(
        max_length=250,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"placeholder": ("Last Name")}
        )
    )
    def save(self, request):

        user = super().save(request)


        return user



class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'slug_user']
        widgets = {
            'avatar': CustomClearableFileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*'
            }),
        }


class CustomAddEmailForm(AddEmailForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customize fields here
        self.fields['email'].label = "New Email Address"
        self.fields['email'].widget = forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your new email',
        })

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if "spam" in email:
            raise forms.ValidationError("Invalid email address.")
        return email