from django.http import HttpResponse
from django.shortcuts import render


from .scrape import initial_player_lookup, lookup_player_stats
from .models import Player, PlayerData, Game
from .engine import predict_players_live, post_engine


def players(request):
    context = {'players': Player.objects.all()}
    #initial_player_lookup()
    #lookup_player_stats('qb')
    return render(request, 'data_grabber/players.html', context)

def player_detail(request, player_id):
    player_data = PlayerData.objects.filter(player__pk=player_id).order_by('game__game_date')
    return render(request, 'data_grabber/player_detail.html', {'player_data': player_data})

def game_detail(request, game_id):
    game_data = Game.objects.filter(pk=game_id).order_by('game_date')
    return render(request, 'data_grabber/game_detail.html', {'game_data': game_data})

def predictions(request):
    raw_preds = predict_players_live()
    final_preds = post_engine(raw_preds)
    return render(request, 'data_grabber/predictions.html', {'predictions': final_preds})
