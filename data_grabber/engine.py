from .models import Player, Game, PlayerData


def pre_engine():
    # creates classifiers necessary for engine.
    return True

def engine():
    # given the inputs, runs model to pick top player for the week
    return True

def post_engine():
    # takes chosen player and produces the necessary info to send to front-end view
    return True

def espn_scoring_rules():
    # produces the score for the player each week
    return True

def test_control_split():
    # train model with weeks 1-13 and predict for week 14
    return True
