
from allauth.account.adapter import DefaultAccountAdapter
from django.urls import reverse
class AccountAdapter(DefaultAccountAdapter):
    
    def save_user(self, request, user, form, commit=True):

        data = form.cleaned_data
        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        user.email = data["email"]
        
       
        
        
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
            
        self.populate_username(request, user)
        
        user.save()
        return user
    
    def get_login_redirect_url(self, request):
        user = request.user
        return reverse("profile", kwargs={"slug_user": user.slug_user})
        