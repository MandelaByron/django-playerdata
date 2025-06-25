
from django.http import HttpRequest
from django.http.response import HttpResponse as HttpResponse
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import DetailView, UpdateView, TemplateView
from users.models import User
from allauth.account.views import EmailView
from .forms import ProfileUpdateForm,CustomAddEmailForm
def profile_view(request):

    return render(request, template_name="users/profile.html")

class ProfileDetailView(DetailView):
    model = User

    context_object_name = "user"

    template_name = "users/profile.html"
    slug_field = "slug_user"
    slug_url_kwarg = "slug_user"



class SettingsBaseView(UpdateView):
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

# class GeneralsUpdateView(SettingsBaseView):
#     template_name = "users/general-settings.html"
#     htmx_partial = 'users/general-form.html'
#     form_class = EmailAddress
#     active_section = 'general'
#     success_url = reverse_lazy("general-settings")
    

class GeneralsUpdateView(TemplateView):

    template_name = "users/general-settings.html"

    htmx_partial = 'users/general-form.html'

    active_section = 'general'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        if request.headers.get("HX-Request"):
            context["htmx"] = True
            return render(request, self.htmx_partial, context)

        return super().get(request, *args, **kwargs)

class CustomEmailView(EmailView):
    form_class = CustomAddEmailForm

    htmx_partial = 'partials/email-form.html'

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
                return render(request, self.htmx_partial, {"form": form})
            return self.form_invalid(form)