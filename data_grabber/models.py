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

    def __repr__(self):
        return "Team: {}".format(self.team)


class PlayerData(models.Model):
    player = models.ForeignKey(Player)
    game = models.ForeignKey(Game)
    pass_attempts = models.IntegerField(null=True)
    pass_completions = models.IntegerField(null=True)
    pass_yards = models.IntegerField(null=True)
    pass_touchdowns = models.IntegerField(null=True)
    interceptions = models.IntegerField(null=True)
    rush_attempts = models.IntegerField(null=True)
    rush_yards = models.IntegerField(null=True)
    rush_touchdowns = models.IntegerField(null=True)
    rec_yards = models.IntegerField(null=True)
    rec_touchdowns = models.IntegerField(null=True)
    receptions = models.IntegerField(null=True)

    def __repr__(self):
        return "Player_id: {}, Team: {}".format(self.player.pk, self.game.team)
