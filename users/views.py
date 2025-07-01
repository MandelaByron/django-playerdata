from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
import time
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, TemplateView
from users.models import User
from allauth.account.views import EmailView, PasswordChangeView
from .forms import ProfileUpdateForm,CustomAddEmailForm, SinglePasswordChangeForm
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin


def search_username(request):
    query = request.GET.get("slug_user", "")
    user = User.objects.filter(slug_user=query).first()
    time.sleep(1)
    return render(request, 'partials/search-feedback.html', {
        "user_found": bool(user)
    })

class ProfileDetailView(LoginRequiredMixin,DetailView):
    model = User

    context_object_name = "user"

    template_name = "users/profile.html"
    slug_field = "slug_user"
    slug_url_kwarg = "slug_user"



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
        messages.success(self.request, "Settings updated successfully.")
        return super().form_valid(form)


class ProfileUpdateView(SettingsBaseView):
    template_name = "users/profile-settings.html"
    htmx_partial = "users/profile-form.html"
    form_class = ProfileUpdateForm
    active_section = "profile"
    success_url = reverse_lazy("profile-settings")

    

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
            print("invalid-form")
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
