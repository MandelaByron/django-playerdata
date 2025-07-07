from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Player

class PlayerDetailView(DetailView):
    model = Player

    context_object_name = 'player'

    template_name = 'players/player_detail.html'

    slug_field = "id"
    
    slug_url_kwarg = "id"

