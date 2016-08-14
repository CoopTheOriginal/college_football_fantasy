from django.http import HttpResponse
from django.shortcuts import render

from .scrape import populate_players, lookup_player_stats
from .models import Player, PlayerData, Game
from .engine import predict_players_live, post_engine


def players(request):
    context = {'players': Player.objects.all()}

    populate_players('WR', 2016)
    # lookup_player_stats('QB')
    return render(request, 'data_grabber/players.html', context)

def player_detail(request, player_id):
    player_data = PlayerData.objects.filter(player__pk=player_id).order_by('game__game_date')
    return render(request, 'data_grabber/player_detail.html', {'player_data': player_data})

def game_detail(request, game_id):
    game_data = Game.objects.filter(pk=game_id).order_by('game_date')
    return render(request, 'data_grabber/game_detail.html', {'game_data': game_data})

def predictions(request):
    raw_preds = predict_players_live(14)
    final_preds = post_engine(raw_preds, 14)
    return render(request, 'data_grabber/predictions.html', {'predictions': final_preds})
