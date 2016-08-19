from flask import Blueprint, flash, render_template
from .forms import LoginForm, RegistrationForm
from flask.ext.login import login_user, logout_user
from flask.ext.login import login_required, current_user

from .scrape import main_populate_all, lookup_all_player_stats

weekly_college_fantasy = Blueprint("weekly_college_fantasy", __name__)


@weekly_college_fantasy.route("/")
def index():
    ## Populates and/or updates the list of players/kickers/defenses
    #main_populate_all(2016)
    ## Collects and stores latest stats for all players
    lookup_all_player_stats('QB')
    return render_template('index.html')

@weekly_college_fantasy.route("/players")
def players():

    player_data = [1,2,3]
    return render_template('players.html', player_data=player_data)


@weekly_college_fantasy.route("/game/<game_id>")
def game_detail(request, game_id):
    #game_data = Game.objects.filter(pk=game_id).order_by('game_date')
    game_data = [1,2,3,4]
    return render(request, 'game_detail.html', {'game_data': game_data})


@weekly_college_fantasy.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("That email or password is not correct.")
    flash_errors(form)
    return render_template("login.html", form=form)


def flash_errors(form, category="warning"):
    '''Flash all errors for a form.'''
    for field, errors in form.errors.items():
        for error in errors:
            flash("{0} - {1}"
                    .format(getattr(form, field).label.text, error), category)
