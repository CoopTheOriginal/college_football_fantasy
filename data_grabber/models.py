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
    game_date = models.CharField(max_length=50)
    opponent = models.CharField(max_length=100)
    your_score = models.IntegerField()
    opponent_score = models.IntegerField()

    def __repr__(self):
        return "Team: {}".format(self.team)


class Passing(models.Model):
    player_id = models.ForeignKey(Player)
    attempts = models.IntegerField()
    completions = models.IntegerField()
    yards = models.IntegerField()
    touchdowns = models.IntegerField()

    def __repr__(self):
        return "Pass Attempts: {}".format(self.attempts)


class Rushing(models.Model):
    player_id = models.ForeignKey(Player)
    attempts = models.IntegerField()
    yards = models.IntegerField()
    touchdowns = models.IntegerField()

    def __repr__(self):
        return "Rush Attempts: {}".format(self.attempts)
