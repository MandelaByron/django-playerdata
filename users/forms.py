
from allauth.account.forms import SignupForm, AddEmailForm
from django import forms
from django.contrib.auth.forms import UserChangeForm
from users.models import User
from .widgets import CustomClearableFileInput
from allauth.account.models import EmailAddress
from allauth.account.forms import SetPasswordField, ChangePasswordForm
from allauth.account.internal import flows
from django.contrib.auth import update_session_auth_hash
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

    slug_user = forms.SlugField(
        error_messages= {
            'unique':'This username is already taken. Please choose another one.'
        },

        required= True
    )
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
        value = super().clean_email()

        # Additional enforcement: make sure the email isn't in use by others
        if EmailAddress.objects.filter(email=value).exclude(user=self.user).exists():
            raise forms.ValidationError("This email is not valid or available for use.")

        return value
    
class SinglePasswordChangeForm(ChangePasswordForm):
    password = SetPasswordField(label=("New Password"))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Only keep password1 field
        self.fields = {
            "password": self.fields["password"],
        }

        # Set user for password validation
        self.fields["password"].user = self.user

    def save(self, request=None, *args, **kwargs):
        flows.password_change.change_password(self.user, self.cleaned_data["password"])
        if request:
            update_session_auth_hash(request, self.user)
        return self.user
