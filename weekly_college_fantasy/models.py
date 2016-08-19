from .extensions import db
from .extensions import bcrypt, login_manager
from flask.ext.login import UserMixin


@login_manager.user_loader
def load_user(id):
    return User.query.get(id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(60))

    def get_password(self):
        return getattr(self, "_password", None)
        return self._password

    def set_password(self, password):
        self._password = password
        self.encrypted_password = bcrypt.generate_password_hash(password)

    password = property(get_password, set_password)

    def check_password(self, password):
        return bcrypt.check_password_hash(self.encrypted_password, password)

    def __repr__(self):
        return "<User {}>".format(self.email)


class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(120))
    team = db.Column(db.String(120))
    position = db.Column(db.String(120))
    year = db.Column(db.Integer)
    ext_id = db.Column(db.Integer)
    player_data = db.relationship('PlayerData', backref='player',
                                lazy='dynamic')

    def __repr__(self):
        return "<Player Name: {}>".format(self.name)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    team = db.Column(db.String(120))
    game_date = db.Column(db.DateTime)
    opponent = db.Column(db.String(120))
    your_score = db.Column(db.Integer)
    opponent_score = db.Column(db.Integer)
    home = db.Column(db.Boolean)
    week = db.Column(db.Integer)
    season = db.Column(db.Integer)
    player_data = db.relationship('PlayerData', lazy='dynamic')

    def __repr__(self):
        return "<Team: {}, Week: {}>".format(self.team, self.week)


class PlayerData(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    player_id = db.Column(db.Integer, db.ForeignKey('player.id'))
    game = db.Column(db.Integer, db.ForeignKey('game.id'))
    pass_attempts = db.Column(db.Integer, default=0)
    pass_completions = db.Column(db.Integer, default=0)
    pass_yards = db.Column(db.Integer, default=0)
    pass_touchdowns = db.Column(db.Integer, default=0)
    interceptions = db.Column(db.Integer, default=0)
    rush_attempts = db.Column(db.Integer, default=0)
    rush_yards = db.Column(db.Integer, default=0)
    rush_touchdowns = db.Column(db.Integer, default=0)
    rec_yards = db.Column(db.Integer, default=0)
    rec_touchdowns = db.Column(db.Integer, default=0)
    receptions = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    predicted = db.Column(db.Integer, default=0)
    extra_point_kick = db.Column(db.Integer, default=0)
    three_point_kick = db.Column(db.Integer, default=0)

    def __repr__(self):
        return "<Player_Ext_id: {}, Team: {}, Week: {}>".format(self.player.ext_id, self.game.team, self.game.week)
