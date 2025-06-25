from django.urls import path
from .views import  ProfileDetailView, ProfileUpdateView, GeneralsUpdateView, CustomEmailView

urlpatterns = [
    #path("manage/", ProfileUpdateView.as_view(), name="profile_update"),
    path("settings/", ProfileUpdateView.as_view(), name="profile-settings"),
    path("settings/general", GeneralsUpdateView.as_view(), name="general-settings"),
    path("accounts/email/", CustomEmailView.as_view(), name="account_email"),
    path("<slug:slug_user>/", ProfileDetailView.as_view(), name="profile"),

]