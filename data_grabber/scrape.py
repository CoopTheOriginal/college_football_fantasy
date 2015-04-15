import http.client
from bs4 import BeautifulSoup
from .models import Player, Game, PlayerData
import re
import datetime


def url_request(partial_path):
    path = '/collegefootball/' + partial_path
    server = http.client.HTTPConnection('www.cbssports.com')
    server.putrequest('GET', path)
    server.putheader('Accept', 'text/html')
    server.endheaders()
    reply = server.getresponse()
    if reply.status != 200:
        return 'Error sending request {0} {1}'.format(reply.status, reply.reason)
    else:
        soup_object = BeautifulSoup(reply.read())
        reply.close()
        return soup_object

def initial_player_lookup(position='qb'):
    position_url = {'qb':'PTDS', 'rb':'RYDS', 'wr':'RECTDS'}
    position_path = 'stats/leaders/sortableTable/NCAAF/' + position_url[position] + \
                                            '/regularseason?&print_rows=9999'
    souped_page = url_request(position_path)
    first_group = souped_page.find_all('tr', attrs={'class': 'row2'})
    second_group = souped_page.find_all('tr', attrs={'class': 'row1'})
    all_players = []
    all_players.extend(first_group[:75])
    all_players.extend(second_group[:75])
    for player in all_players:
        save_player_data(player, position)


def save_player_data(bs_chunk, position):
    ext_id = re.sub(r'\D', "", bs_chunk.find('a')['href'])
    if not Player.objects.filter(ext_id=ext_id):
        each_player = bs_chunk.find_all('td')
        new = Player(ext_id=ext_id,
                     name=each_player[1].text,
                     team=each_player[2].text,
                     position=position,
                     year=2014)
        new.save()

def player_name_cleanup(player):
    player_name = player.name.replace('.', '')
    return player_name.replace(' ', '-')

def game_date_cleanup(game_date):
    if '01/' in game_date:
        game_date += '/' + str(datetime.datetime.now().year)
    else:
        game_date += '/' + str(datetime.datetime.now().year - 1)
    new_date = datetime.datetime.strptime(game_date, '%m/%d/%Y').date()
    return new_date

def quarterback_stat_lookup(player):
    print('player', player.name)
    player_name = player_name_cleanup(player)
    souped_page = url_request('players/playerpage/' + str(player.ext_id) + '/' + player_name)
    souped_page = souped_page.find('table', attrs={'class': 'borderTop'})
    if souped_page.find_all(text='Passing'):
        all_stats = souped_page.find_all('tr', attrs={'class': 'row1'})
        all_stats.extend(souped_page.find_all('tr', attrs={'class': 'row2'}))

        for stat in all_stats[1:]:
            each_stat = stat.find_all('td')
            score = score_breakout(each_stat[2].text)
            game_date = game_date_cleanup(each_stat[0].text)
            home_away, opp = home_check(each_stat[1].text)
            game_obj, created = Game.objects.get_or_create(team=player.team,
                                                           game_date=game_date,
                                                           opponent=opp,
                                                           your_score=score[0],
                                                           opponent_score=score[1],
                                                           home=home_away,
                                                           week=determine_week(game_date))
            if created:
                player_stats = PlayerData(player=player,
                                          game=game_obj,
                                          pass_attempts=each_stat[3].text,
                                          pass_completions=each_stat[4].text,
                                          pass_yards=each_stat[6].text,
                                          pass_touchdowns=each_stat[8].text,
                                          interceptions=each_stat[9].text,
                                          rush_attempts=each_stat[10].text,
                                          rush_yards=each_stat[11].text,
                                          rush_touchdowns=each_stat[13].text,
                                          score=0)
                espn_scoring_rules(player_stats)
                player_stats.save()

def lookup_player_stats(player_position):
    all_players = Player.objects.filter(position=player_position)
    for player in all_players:
        if not PlayerData.objects.filter(player=player):
            quarterback_stat_lookup(player)


def score_breakout(score):
    return re.findall(r'\d+', score)

def determine_week(a_date):
    weeks = dict()
    d7 = datetime.timedelta(days = 7)
    iterDay = datetime.date(2014,8,26)
    counter = 1
    while iterDay <= datetime.date(2015, 1, 13):
        end_date =  iterDay + d7
        weeks[counter] = (iterDay, end_date)
        iterDay += d7
        counter += 1

    for week, date_range in weeks.items():
        if date_range[0] <= a_date <= date_range[1]:
            return week

def home_check(opponent_text):
    if '@' in opponent_text:
        return False, opponent_text.replace('@', '')
    else:
        return True, opponent_text


def espn_scoring_rules(a_player):
    a_player.score += (6 * a_player.rush_touchdowns)
    a_player.score += (4 * a_player.pass_touchdowns)
    if a_player.rush_yards > 0:
        a_player.score += (a_player.rush_yards // 10)
    a_player.score += (a_player.pass_yards // 25)
    a_player.score += (6 * a_player.rec_touchdowns)
    a_player.save()
    return a_player
