from django.http import JsonResponse, HttpResponseBadRequest
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from allauth.account.models import EmailAddress
import time
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, TemplateView, DeleteView
from users.models import User
from allauth.account.views import EmailView, PasswordChangeView
from .forms import ProfileUpdateForm,CustomAddEmailForm, SinglePasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.decorators import login_required

def search_username(request):
    query = request.GET.get("username", "")
    user = User.objects.filter(username=query).first()
    time.sleep(1)
    return render(request, 'partials/search-feedback.html', {
        "user_found": bool(user)
    })

@login_required
def cancel_email_change(request):
    if request.method != "POST":
        return HttpResponseBadRequest("Invalid request method.")

    email_to_cancel = request.POST.get("email")
    user = request.user

    if not email_to_cancel:
        messages.error("Email entered is invalid")
        return render(request, "partials/email-button.html")

    try:
        email_obj = EmailAddress.objects.get(user=user, email=email_to_cancel, verified=False)
    except EmailAddress.DoesNotExist:
        messages.error("Email entered is invalid")
        return render(request, "partials/email-button.html")

    email_obj.remove()
    messages.success(request, "Your email change request has been canceled.")
    return render(request, "partials/email-button.html")

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = User

    context_object_name = "user"

    template_name = "users/profile.html"
    slug_field = "username"
    slug_url_kwarg = "username"



class SettingsBaseView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = ""
    form_class = None
    active_section = ""
    htmx_partial = ""

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_section"] = self.active_section
        context['title'] = 'Profile Settings'
        return context

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data()
        
        if request.headers.get("HX-Request"):
            context["htmx"] = True
            return render(request, self.htmx_partial, context)

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        from django.contrib import messages
        messages.success(self.request, "Profile updated successfully.")
        return super().form_valid(form)


class ProfileUpdateView(SettingsBaseView):
    template_name = "users/profile-settings.html"
    htmx_partial = "users/profile-form.html"
    form_class = ProfileUpdateForm
    active_section = "profile"
    success_url = reverse_lazy("profile-settings")

    # def test_func(self) -> bool | None:
    #     user = self.get_object()
    #     return user

    

class GeneralsUpdateView(LoginRequiredMixin,TemplateView):

    template_name = "users/general-settings.html"

    htmx_partial = 'users/general-form.html'

    active_section = 'general'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_section"] = self.active_section
        context['title'] = 'Account Settings'
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            context["htmx"] = True
            return render(request, self.htmx_partial, context)

        return super().get(request, *args, **kwargs)

class CustomEmailView(LoginRequiredMixin, EmailView):
    form_class = CustomAddEmailForm

    htmx_partial = 'partials/email-form.html'

    template_name = 'users/general-settings.html'



    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            context["htmx"] = True
            return render(request, self.htmx_partial, context)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()
        if form.is_valid():
            form.save(request)  # this adds the new email
            if request.headers.get("HX-Request"):
                return render(request, "partials/email-pending.html", {
                    "email": form.cleaned_data["email"]
                })
            return redirect("account_email")
        else:
            if request.headers.get("HX-Request"):
                messages.error(self.request, "This email is not valid or available for use.")
                return render(request, "partials/email-button.html", {"status": "invalid"})
            else:
                messages.error(self.request, "This email is not valid or available for use.")

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    htmx_partial = 'partials/password-change-form.html'

    template_name = 'users/general-settings.html'

    form_class = SinglePasswordChangeForm

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()

        if request.headers.get("HX-Request"):
            context["htmx"] = True
            return render(request, self.htmx_partial, context)
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form()

        if form.is_valid():
            form.save(request)
            if request.headers.get("HX-Request"):
                messages.success(self.request,"Password updated successfully")
                return render(request, "partials/password-button.html")
            return redirect("general-settings")
        else:
            print("invalid password form")
            if request.headers.get("HX-Request"):
                messages.error(self.request, "The Password entered is invalid.")
                return render(request, "partials/password-button.html", {"status": "invalid"})
            else:
                messages.error(self.request, "The Password entered is invalid.")

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
   
    success_url = reverse_lazy('account_deleted')
    
    def get_object(self, queryset=None):
        return self.request.user
    

class AccountDeletedView(TemplateView):
    template_name = "account/account_confirm_delete.html"
