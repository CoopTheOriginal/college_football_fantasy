import http.client
from bs4 import BeautifulSoup
from .models import Player, Game, PlayerData
import re
import datetime


SEASON_START = datetime.date(2015,9,2)

def url_request(partial_path):
    path = '/collegefootball/' + partial_path
    server = http.client.HTTPConnection('www.cbssports.com')
    server.putrequest('GET', path)
    server.putheader('Accept', 'text/html')
    server.endheaders()
    reply = server.getresponse()
    if reply.status != 200:
        return 'Error sending request {0} {1}'.format(reply.status,
                                                      reply.reason)
    else:
        soup_object = BeautifulSoup(reply.read())
        reply.close()
        return soup_object


def main_populate_all(year):
    """ Hit website to create/update master list of players/teams for all
    positions."""

    def populate_defense():
        """Hit website to create/update master list of defense"""
        return True

    def populate_players(position):
        position_path = 'stats/playersort/NCAAF/' + position + \
                        '/regularseason?&print_rows=9999'
        souped_page = url_request(position_path)
        first_group = souped_page.find_all('tr', attrs={'class': 'row2'})
        second_group = souped_page.find_all('tr', attrs={'class': 'row1'})
        all_players = []
        all_players.extend(first_group)
        all_players.extend(second_group)

        # Treat TE's as WR
        if position == 'TE': position = 'WR'
        [save_player_data(player, position, year) for player in all_players]

    [populate_players(position) for position in ['WR', 'QB', 'RB', 'TE', 'K']]
    populate_defense()
    return True


def save_player_data(bs_chunk, position, year):
    ext_id = re.sub(r'\D', "", bs_chunk.find('a')['href'])
    each_player = bs_chunk.find_all('td')
    team = each_player[1].text
    if team == '': team = 'not listed'
    Player.objects.get_or_create(ext_id=ext_id,
                                 name=each_player[0].text,
                                 team=team,
                                 position=position,
                                 year=year)



def game_date_cleanup(game_date):
    if '01/' in game_date:
        game_date += '/' + str(datetime.datetime.now().year)
    else:
        game_date += '/' + str(datetime.datetime.now().year - 1)
    new_date = datetime.datetime.strptime(game_date, '%m/%d/%Y').date()
    return new_date


def quarterback_stat_lookup(player):

    def player_name_prep():
        """Preps player.name for URL request"""
        player_name = player.name.replace('.', '')
        return player_name.replace(' ', '-')

    player_name = player_name_prep()
    print('player', player_name)
    souped_page = url_request('players/playerpage/' + str(player.ext_id) \
                              + '/' + player_name)
    souped_page = souped_page.find('table', attrs={'class': 'borderTop'})
    if souped_page.find_all(text='Passing'):
        all_stats = souped_page.find_all('tr', attrs={'class': 'row1'})
        all_stats.extend(souped_page.find_all('tr', attrs={'class': 'row2'}))

        for stat in all_stats[1:]:
            each_stat = stat.find_all('td')
            score = score_breakout(each_stat[2].text)
            game_date = game_date_cleanup(each_stat[0].text)
            home_away, opp = home_check(each_stat[1].text)
            print('week: ', determine_week(game_date))
            game_obj, created = Game.objects.get_or_create(team=player.team,
                                                           game_date=game_date,
                                                           opponent=opp,
                                                           your_score=int(score[0]),
                                                           opponent_score=int(score[1]),
                                                           home=home_away,
                                                           week=determine_week(game_date),
                                                           season=SEASON_START.year)
            if created:
                player_stats = PlayerData(player=player,
                                          game=game_obj,
                                          pass_attempts=int(each_stat[3].text),
                                          pass_completions=int(each_stat[4].text),
                                          pass_yards=int(each_stat[6].text),
                                          pass_touchdowns=int(each_stat[8].text),
                                          interceptions=int(each_stat[9].text),
                                          rush_attempts=int(each_stat[10].text),
                                          rush_yards=int(each_stat[11].text),
                                          rush_touchdowns=int(each_stat[13].text),
                                          score=0)
                player_stats = scoring_rules_main(player_stats)
                player_stats.save()


def lookup_player_stats(player_position):
    all_players = Player.objects.filter(position=player_position)
    for player in all_players:
        if not PlayerData.objects.filter(player=player):
            quarterback_stat_lookup(player)


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


def scoring_rules_main(a_player_obj):
    """Master checker for determining a player dictionary's score"""

    def scoring_rules_player():
        """Takes in a dictionary of a player's (specifically a qb, wr,
        and/or rb) performance and returns the score for that player as
        defined by the rules"""
        score = 0
        score += (6 * a_player_obj.rush_touchdowns)
        score += (4 * a_player_obj.pass_touchdowns)
        if a_player_obj.rush_yards > 0:
            score += (a_player_obj.rush_yards // 10)
        score += (a_player_obj.pass_yards // 25)
        score += (6 * a_player_obj.rec_touchdowns)
        a_player_obj.score = score

    def scoring_rules_kicker():
        """Takes in a dictionary of a kicker's performance and returns the
        score for the kicker as defined by the rules"""
        score = 0
        score += (1 * a_player_obj['1-19'])
        score += (2 * a_player_obj['20-29'])
        score += (3 * a_player_obj['30-39'])
        score += (4 * a_player_obj['40-49'])
        score += (5 * a_player_obj['50+'])
        score += (1 * a_player_obj['XP'])
        a_player_obj.score = score

    def scoring_rules_defense():
        """Takes in a dictionary of a defense's performance and returns the
        score for the defense as defined by the rules"""
        score = 0
        a_player_obj.score = score

    if a_player_obj.player.position == 'K': scoring_rules_kicker()
    elif a_player_obj.player.position == 'DEF': scoring_rules_defense()
    else: scoring_rules_player()
    return a_player_obj
