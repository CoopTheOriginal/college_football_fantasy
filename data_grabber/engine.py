from .models import Player, Game, PlayerData

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import seaborn as sbn
from collections import namedtuple



def team_to_int_dict():
    teams = list(Game.objects.all().values_list('team', flat=True).distinct())
    return {team:teams.index(team) for team in teams}


def prep_model_input(player_list):
    team_ids = team_to_int_dict()
    player_stats =  np.array([[team_ids[stat.game.team],
                               stat.game.home]
                               for stat in player_list])
    player_names = [stat.player.name for stat in player_list]
    return player_stats, player_names


def create_predictions(train_input, train_answer, test_input):
    rfc = RandomForestClassifier ()
    rfc.fit(train_input, train_answer)
    prediction_float = rfc.predict(test_input)
    return [int(num) for num in prediction_float]


def plot_pred_actual(player_stat, predicted, test_answer, player_labels):
    plt.figure(figsize=(13,7))
    plt.title(player_stat)
    plt.plot(test_answer, 'g', label='Actual')
    plt.plot(predicted, 'r', label='Predicted')
    label_length = range(len(player_labels))
    plt.xticks(label_length, player_labels)
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.show()


def get_train_test_players(week):
    train_players = PlayerData.objects.filter(game__week__lte=13)
    test_players = PlayerData.objects.filter(game__week=week)
    return train_players, test_players


def player_stat_arrays(player_list):
    final_dict = player_list[0].to_dict()
    final_dict = {stat_name:np.array([]) for stat_name in final_dict.keys()}
    for player in player_list:
        player_dict = player.to_dict()
        for stat in final_dict.keys():
            new_list = np.append(final_dict[stat], [player_dict[stat]])
            final_dict[stat] = new_list
    return final_dict


def predict_players_backtest():
    train_players, test_players = get_train_test_players()
    train_input, train_player_names = prep_model_input(train_players)
    test_input, test_player_names = prep_model_input(test_players)
    train_players_dict = player_stat_arrays(train_players)
    test_players_dict = player_stat_arrays(test_players)

    for player_stat in train_players_dict.keys():
        predicted = create_predictions(train_input, train_players_dict[player_stat], test_input)
        accuracy = accuracy_score(test_players_dict[player_stat], predicted)
        plot_pred_actual(player_stat, predicted, test_players_dict[player_stat], test_player_names)
        print('{} accuracy score = {}'.format(player_stat, accuracy))
    return final_predictions


def predict_players_live(week):
    train_players, test_players = get_train_test_players(week)
    train_input, train_player_names = prep_model_input(train_players)
    test_input, test_player_names = prep_model_input(test_players)
    train_players_dict = player_stat_arrays(train_players)
    test_players_dict = player_stat_arrays(test_players)

    final_player_pred_dict = {name:{} for name in test_player_names}
    for player_stat in train_players_dict.keys():
        predicted = create_predictions(train_input, train_players_dict[player_stat], test_input)
        accuracy = accuracy_score(test_players_dict[player_stat], predicted)

        for name, prediction in zip(test_player_names, predicted):
            final_player_pred_dict[name][player_stat] = prediction
    return final_player_pred_dict


def post_engine(predict_dict, week):
    final_list = []

    for name, stats in predict_dict.items():
        player = Player.objects.get(name=name)
        game = Game.objects.get(week=week, team=player.team)
        stats['predicted'] = scoring_rules_player(stats)
        plyrdata_obj, created = PlayerData.objects.update_or_create(player=player,
                                                                    game=game,
                                                                    predicted__gte=1,
                                                                    defaults=stats)
        final_list.append(plyrdata_obj)
    return sorted(final_list, key=lambda x : x.predicted, reverse=True)


def scoring_rules_main(a_player_dict):
    """Master checker for determining a player dictionary's score"""
    if a_player_dict['position'] == 'K':
        return scoring_rules_kicker(a_player_dict)
    elif a_player_dict['position'] == 'DEF':
        return scoring_rules_defense(a_player_dict)
    else:
        return scoring_rules_player(a_player_dict)

def scoring_rules_player(a_player_dict):
    """Takes in a dictionary of a player's (specifically a qb, wr,
    and/or rb) performance and returns the score for that player as
    defined by the rules"""
    score = 0
    score += (6 * a_player_dict['rush_touchdowns'])
    score += (4 * a_player_dict['pass_touchdowns'])
    if a_player_dict['rush_yards'] > 0:
        score += (a_player_dict['rush_yards'] // 10)
    score += (a_player_dict['pass_yards'] // 25)
    score += (6 * a_player_dict['rec_touchdowns'])
    return score

def scoring_rules_kicker(a_player_dict):
    """Takes in a dictionary of a kicker's performance and returns the
    score for the kicker as defined by the rules"""
    score = 0
    score += (1 * a_player_dict['1-19'])
    score += (2 * a_player_dict['20-29'])
    score += (3 * a_player_dict['30-39'])
    score += (4 * a_player_dict['40-49'])
    score += (5 * a_player_dict['50+'])
    score += (1 * a_player_dict['XP'])
    return score

def scoring_rules_defense(a_player_dict):
    """Takes in a dictionary of a defense's performance and returns the
    score for the defense as defined by the rules"""
    score = 0
    return score
