import http.client, re, time
from bs4 import BeautifulSoup
import weekly_college_fantasy.helper_functions_scrape as hf
from .models import Player, Game, PlayerData
from .extensions import db


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
        soup_object = BeautifulSoup(reply.read(), "html.parser")
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

        # See if object exists and if it doesn't save it
        if not Player.query.filter_by(ext_id=ext_id, year=year).first():
            print("{} with ext_id: {} was added".format(each_player[0].text,
                                                        ext_id))
            db.session.add(Player(ext_id=ext_id,
                                  name=each_player[0].text,
                                  team=team,
                                  position=position,
                                  year=year))


    def populate_players(position):
        position_path = 'stats/playersort/NCAAF/' + position + \
                        '/regularseason?&print_rows=9999'
        souped_page = url_request(position_path)
        all_players = souped_page.find_all('tr', attrs={'class': 'row2'})
        all_players.extend(souped_page.find_all('tr', attrs={'class': 'row1'}))

        # Treat TE's as WR
        if position == 'TE': position = 'WR'
        [save_player_data(bs_chunk, position) for bs_chunk in all_players]


    for position in ['WR', 'QB', 'RB', 'TE', 'K']:
        print("Populating players for: ", position)
        populate_players(position)
    # Commit all new players to database
    db.session.commit()

    print("Populating players for: Defense")
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
    home_away, opp = hf.home_check(each_stat_list[1].text)
    score = hf.score_breakout(each_stat_list[2].text)
    game_date = hf.game_date_cleanup(each_stat_list[0].text)
    game_info =  {"team": team,
                  "game_date": game_date,
                  "opponent": opp,
                  "your_score": int(score[0]),
                  "opponent_score": int(score[1]),
                  "home": home_away,
                  "week": hf.determine_week(game_date),
                  "season": hf.SEASON_START.year}

    # See if object exists and if it doesn't, save it
    exists = Game.query.filter_by(**game_info).first()
    if exists: return exists
    else:
        print("Game between {} & {} in week {} was added"\
              .format(team, opp, hf.determine_week(game_date)))
        game_obj = Game(**game_info)
        db.session.add(game_obj)
        db.session.commit()
        return game_obj


def position_stat_breakout(each_stat_list, position):
    """Takes in a list of tds from BeautifulSoup and returns dict of
    what stats belong to which values"""

    def kicker_stat_prep(kicker_stat):
        """Breaks out stats where it goes "number-number", into dictionary
        with 'made' and 'total'"""
        numbers = kicker_stat.split('-')
        return {'made': int(numbers[0]), 'total': int(numbers[1])}

    if position == 'QB':
        stat_dict = {"pass_attempts": int(each_stat_list[3].text),
                     "pass_completions": int(each_stat_list[4].text),
                     "pass_yards": int(each_stat_list[6].text),
                     "pass_touchdowns": int(each_stat_list[8].text),
                     "interceptions": int(each_stat_list[9].text),
                     "rush_attempts": int(each_stat_list[10].text),
                     "rush_yards": int(each_stat_list[11].text),
                     "rush_touchdowns": int(each_stat_list[13].text)
                     }
    elif position == 'RB':
        stat_dict = {"rush_attempts": int(each_stat_list[3].text),
                     "rush_yards": int(each_stat_list[4].text),
                     "rush_touchdowns": int(each_stat_list[6].text),
                     "receptions": int(each_stat_list[7].text),
                     "rec_yards": int(each_stat_list[8].text),
                     "rec_touchdowns": int(each_stat_list[10].text)
                     }
    elif position == 'WR':
        stat_dict = {"receptions": int(each_stat_list[3].text),
                     "rec_yards": int(each_stat_list[4].text),
                     "rec_touchdowns": int(each_stat_list[6].text),
                     "rush_attempts": int(each_stat_list[7].text),
                     "rush_yards": int(each_stat_list[8].text),
                     "rush_touchdowns": int(each_stat_list[10].text)
                     }
    elif position == 'K':
        extra_point_kick = kicker_stat_prep(each_stat_list[11].text)
        three_point_kick = kicker_stat_prep(each_stat_list[3].text)
        stat_dict = {"extra_point_kick": extra_point_kick['made'],
                     "three_point_kick": three_point_kick['made']
                     }
    return stat_dict


def player_lookup_main(player):
    """Master function for logging a player's performance for every week
    it can find for the current season."""
    player_name = hf.player_name_prep(player.name)
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


def lookup_all_player_stats(player_position):
    all_players = Player.query.filter_by(position=player_position)
    for player in all_players:
        player_lookup_main(player)
        time.sleep(3)


def scoring_rules_main(a_player_dict, position):
    """Master checker for determining a player dictionary's score"""

    def scoring_rules_player():
        """Takes in a dictionary of a player's (specifically a qb, wr,
        and/or rb) performance and returns the score for that player as
        defined by the rules"""
        score = 0
        score += (6 * a_player_dict['rush_touchdowns'])
        if a_player_dict['rush_yards'] > 0:
            score += (a_player_dict['rush_yards'] // 10)
        if position == 'QB':
            score += (4 * a_player_dict['pass_touchdowns'])
            score += (a_player_dict['pass_yards'] // 25)
        else:
            score += (6 * a_player_dict['rec_touchdowns'])
            score += (a_player_dict['rec_yards'] // 10)
        return score

    def scoring_rules_kicker():
        """Takes in a dictionary of a kicker's performance and returns the
        score for the kicker as defined by the rules"""
        score = 0
        score += (1 * a_player_dict['extra_point_kick'])
        score += (3 * a_player_dict['three_point_kick'])
        return score

    def scoring_rules_defense():
        """Takes in a dictionary of a defense's performance and returns the
        score for the defense as defined by the rules"""
        score = 0
        return score

    if position == 'K': return scoring_rules_kicker()
    elif position == 'DEF': return scoring_rules_defense()
    else: return scoring_rules_player()
