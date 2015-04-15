from .models import Player, Game, PlayerData

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import cross_val_score


def pre_engine():
    # creates classifiers necessary for engine.
    return True

def engine():
    # given the inputs, runs model to pick top player for the week
    return True

def post_engine():
    # takes chosen player and produces the necessary info to send to front-end view
    return True

def test_control_split():
    # train model with weeks 1-13 and predict for week 14
    return True

def create_class_array(player_list):
    class_input = np.array([[player_stat.pass_attempts,
                             player_stat.pass_completions,
                             player_stat.pass_yards,
                             player_stat.pass_touchdowns,
                             player_stat.interceptions,
                             player_stat.rush_attempts,
                             player_stat.rush_yards,
                             player_stat.rush_touchdowns] for player_stat in player_list])
    class_answer = np.array([player_stat.score for player_stat in player_list])
    return class_input, class_answer

def engine_validation_scoring():
    train_input, train_answer = create_class_array(PlayerData.objects.filter(game__week__lte=13))
    test_input, test_answer = create_class_array(PlayerData.objects.filter(game__week=14))
    rfc = RandomForestClassifier ()
    rfc.fit(train_input, train_answer)
    predicted = rfc.predict(test_input)
    return accuracy_score(test_answer, predicted)
