import http.client, re
from bs4 import BeautifulSoup
from .helper_functions_scrape import *
from .models import Player, Game, PlayerData
import toolz.curried as tz


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

    def save_player_data(bs_chunk, position):
        ext_id = re.sub(r'\D', "", bs_chunk.find('a')['href'])
        each_player = bs_chunk.find_all('td')
        team = each_player[1].text
        if team == '': team = 'not listed'
        Player.objects.get_or_create(ext_id=ext_id,
                                     name=each_player[0].text,
                                     team=team,
                                     position=position,
                                     year=year)

    def populate_players(position):
        position_path = 'stats/playersort/NCAAF/' + position + \
                        '/regularseason?&print_rows=9999'
        souped_page = url_request(position_path)
        all_players = souped_page.find_all('tr', attrs={'class': 'row2'})
        all_players.extend(souped_page.find_all('tr', attrs={'class': 'row1'}))

        # Treat TE's as WR
        if position == 'TE': position = 'WR'

        [save_player_data(bs_chunk, position) for bs_chunk in all_players]

    [populate_players(position) for position in ['WR', 'QB', 'RB', 'TE', 'K']]
    populate_defense()
    return True




def url_stats_request(player_name, ext_id):
    """Returns a souped page of the player"""
    souped_page = url_request('players/playerpage/' + str(ext_id) + '/' + \
                              player_name)
    souped_page = souped_page.find('table', attrs={'class': 'borderTop'})

    player_stats = souped_page.find_all('tr', attrs={'class': 'row1'})
    player_stats.extend(souped_page.find_all('tr', attrs={'class': 'row2'}))
    labels = souped_page.find_all('tr', attrs={'class': 'label'})
    return labels, player_stats[1:]


def create_game_obj(each_stat_list, team):
    """Takes in a list of 'td' values associated with a row of data
    and returns a dictionary of score, game_date, home_away, season,
    and week"""
    home_away, opp = home_check(each_stat_list[1].text)
    score = score_breakout(each_stat_list[2].text)
    game_date = game_date_cleanup(each_stat_list[0].text)
    game_info =  {"team": team,
                  "game_date": game_date,
                  "opponent": opp,
                  "your_score": int(score[0]),
                  "opponent_score": int(score[1]),
                  "home": home_away,
                  "week": determine_week(game_date),
                  "season": SEASON_START.year}
    game_obj, created = Game.objects.get_or_create(game_info)
    return game_obj


def position_stat_breakout(each_stat_list, position):
    """Takes in a list of tds and returns dict of what stats belong to
    which values"""
    if position == 'QB':
        stat_dict = {"pass_attempts": int(each_stat_list[3].text),
                     "pass_completions": int(each_stat_list[4].text),
                     "pass_yards": int(each_stat_list[6].text),
                     "pass_touchdowns": int(each_stat_list[8].text),
                     "interceptions": int(each_stat_list[9].text),
                     "rush_attempts": int(each_stat_list[10].text),
                     "rush_yards": int(each_stat_list[11].text),
                     "rush_touchdowns": int(each_stat_list[13].text)}
    elif position == 'RB':
        stat_dict = {"rush_attempts": int(each_stat_list[10].text),
                     "rush_yards": int(each_stat_list[11].text),
                     "rush_touchdowns": int(each_stat_list[13].text)}

    return stat_dict



def player_lookup_main(player):
    """Master function for logging a player's performance for every week
    it can find for the current season. """
    player_name = player_name_prep(player.name)
    print('player: {}, ext_id: {}'.format(player_name, player.ext_id))
    labels, player_stats = url_stats_request(player_name, player.ext_id)

    for stat in player_stats:
        each_stat = stat.find_all('td')
        game_obj = create_game_obj(each_stat, player.team)
        player_dict = position_stat_breakout(each_stat, player.position)
        player_dict['score'] = scoring_rules_main(player_dict, player.position)
        player_data, created = PlayerData.objects.update_or_create(
                                player=player,
                                game=game_obj,
                                defaults=player_dict)



def lookup_player_stats(player_position):
    all_players = Player.objects.filter(position=player_position)
    for player in all_players:
        player_lookup_main(player)


def scoring_rules_main(a_player_dict, position):
    """Master checker for determining a player dictionary's score"""

    def scoring_rules_player():
        """Takes in a dictionary of a player's (specifically a qb, wr,
        and/or rb) performance and returns the score for that player as
        defined by the rules"""
        score = 0
        score += (6 * a_player_dict['rush_touchdowns'])
        score += (4 * a_player_dict['pass_touchdowns'])
        if a_player_dict['rush_yards'] > 0:
            score += (a_player_dict['rush_yards'] // 10)
        score += (a_player_dict['pass_yards'] // 25)
        if position != 'QB':
            score += (6 * a_player_dict['rec_touchdowns'])
        return score

    def scoring_rules_kicker():
        """Takes in a dictionary of a kicker's performance and returns the
        score for the kicker as defined by the rules"""
        score = 0
        score += (1 * a_player_dict['1-19'])
        score += (2 * a_player_dict['20-29'])
        score += (3 * a_player_dict['30-39'])
        score += (4 * a_player_dict['40-49'])
        score += (5 * a_player_dict['50+'])
        score += (1 * a_player_dict['XP'])
        return score

    def scoring_rules_defense():
        """Takes in a dictionary of a defense's performance and returns the
        score for the defense as defined by the rules"""
        score = 0
        return score

    if position == 'K': return scoring_rules_kicker()
    elif position == 'DEF': return scoring_rules_defense()
    else: return scoring_rules_player()
