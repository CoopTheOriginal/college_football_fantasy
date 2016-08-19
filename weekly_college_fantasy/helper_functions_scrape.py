import datetime, re


SEASON_START = datetime.date(2015,9,2)


def player_name_prep(name):
    """Preps player.name for URL request"""
    player_name = name.replace('.', '')
    return player_name.replace(' ', '-')


def game_date_cleanup(game_date):
    """ Takes in a game date string and returns cleaned game date string"""
    if '01/' in game_date:
        game_date += '/' + str(datetime.datetime.now().year)
    else:
        game_date += '/' + str(datetime.datetime.now().year - 1)
    new_date = datetime.datetime.strptime(game_date, '%m/%d/%Y').date()
    return new_date


def score_breakout(score):
    return re.findall(r'\d+', score)


def determine_week(a_date):
    """Returns the week in the college football season that the 'a_date'
    took place."""
    def week_dict():
        """Generates a dictionary defining the start and end date of each
        week for the season."""
        weeks = {}
        d7 = datetime.timedelta(days=7)
        iterDay = SEASON_START
        counter = 1
        while iterDay <= datetime.datetime.now().date():
            end_date =  iterDay + d7
            weeks[counter] = (iterDay, end_date)
            iterDay += d7
            counter += 1
        return weeks

    weeks = week_dict()
    for week, date_range in weeks.items():
        if date_range[0] <= a_date <= date_range[1]:
            return week


def home_check(opponent_text):
    if '@' in opponent_text:
        return False, opponent_text.replace('@', '')
    else:
        return True, opponent_text
