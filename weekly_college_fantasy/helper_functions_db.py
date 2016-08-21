from .models import Player, Game, PlayerData
from .extensions import db

def player_data_update_or_create(model_dict):
    """Takes in a PlayerData dictionary. Checks database to update it
    based on the player and game ids. If it doesn't exist, it will create
    a new object"""
    filters = {"game_id": model_dict['game_id'],
               "player_id": model_dict['player_id']}
    exists = PlayerData.query.filter_by(**filters).first()

    if exists:
        player_data = PlayerData.query.get(exists.id)
        for key,value in model_dict.items():
            setattr(player_data, key, value)
        db.session.commit()
    else:
        new_response = PlayerData(**model_dict)
        db.session.add(new_response)
        db.session.commit()
