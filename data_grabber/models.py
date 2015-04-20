from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    team = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    year = models.IntegerField()
    ext_id = models.IntegerField()

    def __repr__(self):
        return "Name: {}".format(self.name)


class Game(models.Model):
    team = models.CharField(max_length=100)
    game_date = models.DateField()
    opponent = models.CharField(max_length=100)
    your_score = models.IntegerField()
    opponent_score = models.IntegerField()
    home = models.BooleanField()
    week = models.IntegerField()

    def __repr__(self):
        return "Team: {}".format(self.team)


class PlayerData(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    pass_attempts = models.IntegerField(default=0)
    pass_completions = models.IntegerField(default=0)
    pass_yards = models.IntegerField(default=0)
    pass_touchdowns = models.IntegerField(default=0)
    interceptions = models.IntegerField(default=0)
    rush_attempts = models.IntegerField(default=0)
    rush_yards = models.IntegerField(default=0)
    rush_touchdowns = models.IntegerField(default=0)
    rec_yards = models.IntegerField(default=0)
    rec_touchdowns = models.IntegerField(default=0)
    receptions = models.IntegerField(default=0)
    score = models.IntegerField(default=0)

    def __repr__(self):
        return "Player_id: {}, Team: {}".format(self.player.pk, self.game.team)

    def to_dict(self):
        del_list = ['score', '_game_cache', '_state', 'player_id',
                    '_player_cache', 'id', 'game_id']
        clean_dict = self.__dict__.copy()
        for bad_attr in del_list:
            if bad_attr in clean_dict.keys():
                del clean_dict[bad_attr]
        return clean_dict
