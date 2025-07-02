from django.urls import path
from .views import  ProfileDetailView, ProfileUpdateView, GeneralsUpdateView, CustomEmailView,AccountDeleteView, AccountDeletedView ,search_username, cancel_email_change,CustomPasswordChangeView

urlpatterns = [
    #path("manage/", ProfileUpdateView.as_view(), name="profile_update"),
    path("search/", search_username, name='search-username'),
    path("settings/", ProfileUpdateView.as_view(), name="profile-settings"),
    path("settings/general", GeneralsUpdateView.as_view(), name="general-settings"),
    path("accounts/email/", CustomEmailView.as_view(), name="account_email"),
    path("accounts/password/change/", CustomPasswordChangeView.as_view(), name='account_change_password'),
    path('accounts/delete-account/', AccountDeleteView.as_view(), name='account_delete'),
    path('accounts/deleted-account/', AccountDeletedView.as_view(), name='account_deleted'),
    path("cancel-email-change/", cancel_email_change, name="cancel-email-change"),
    path("<slug:username>/", ProfileDetailView.as_view(), name="profile"),



]