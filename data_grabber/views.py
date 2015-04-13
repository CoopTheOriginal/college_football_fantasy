from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.core.urlresolvers import reverse


from .scrape import initial_player_lookup, lookup_specific_stats
from .models import Player, PlayerData


def index(request):
    context = {'players': Player.objects.all()}
    initial_player_lookup()
    lookup_specific_stats('qb')
    return render(request, 'data_grabber/index.html', context)

def detail(request, player_id):
    player_data = PlayerData.objects.filter(player__pk=player_id)
    return render(request, 'data_grabber/detail.html', {'player_data': player_data})
