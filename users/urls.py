from django.urls import path
from .views import  ProfileDetailView, ProfileUpdateView, GeneralsUpdateView, CustomEmailView, search_username, CustomPasswordChangeView

urlpatterns = [
    #path("manage/", ProfileUpdateView.as_view(), name="profile_update"),
    path("search/", search_username, name='search-username'),
    path("settings/", ProfileUpdateView.as_view(), name="profile-settings"),
    path("settings/general", GeneralsUpdateView.as_view(), name="general-settings"),
    path("accounts/email/", CustomEmailView.as_view(), name="account_email"),
    path("accounts/password/change/", CustomPasswordChangeView.as_view(), name='account_change_password' ),
    path("<slug:slug_user>/", ProfileDetailView.as_view(), name="profile"),


]