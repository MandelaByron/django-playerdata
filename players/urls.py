from django.urls import path
from .views import PlayerDetailView

urlpatterns = [
    path("detail/<int:id>", PlayerDetailView.as_view(), name='player-detail')
]
