import http.client
from bs4 import BeautifulSoup
from ..extensions import db
from ..models import Player, Passing, Game
import re



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


def lat_long_lookup(bsoup_item):
    location = bsoup_item.find('div', attrs={'class' : 'viewposting'})
    if location:
        item_lat = location["data-latitude"].split("data-latitude=")[-1]
        item_long = location["data-longitude"].split("data-longitude=")[-1]
        return item_lat, item_long
    else:
        return (None, None)


def item_lookup(bsoup_item):

    ind_page = url_request(bsoup_item)
    souped_item = BeautifulSoup(ind_page)

    item_name = name_lookup(souped_item)
    item_url = 'http://raleigh.craigslist.com{}'.format(bsoup_item)
    item_dates = date_lookup(souped_item)
    item_images = image_lookup(souped_item)
    item_lat, item_long = lat_long_lookup(souped_item)
    item_description = description_lookup(souped_item)

    return (item_name, item_url, item_dates, item_images,
            item_lat, item_long, item_description)


def initial_player_lookup(position='qb'):

    position_url = {'qb':'PTDS', 'rb':'RYDS', 'wr':'RECTDS'}
    position_path = 'stats/leaders/NCAAF/' + position_url[position] + \
                                            '/regularseason?&start_row=1'
    souped_page = url_request(position_path)
    all_players = souped_page.find_all('tr', attrs={'class': 'row2'})
    all_players.extend(souped_page.find_all('tr', attrs={'class': 'row1'}))
    for player in all_players:
        ext_id = re.sub(r'\D', "", player.find('a')['href'])

        if not Player.query.filter_by(ext_id=ext_id).first():
            each_player = player.find_all('td')
            player = Player(ext_id=ext_id,
                            name=each_player[1].text,
                            team=each_player[2].text,
                            position=position,
                            year=2014)
            db.session.add(player)
    db.session.commit()

def quarterback_stat_lookup(player):
    player_name = player.name.replace(' ', '-')
    souped_page = url_request('players/playerpage/' + str(player.ext_id) + '/' + player_name)

    all_stats = souped_page.find_all('tr', attrs={'class': 'row1'})
    all_stats.extend(souped_page.find_all('tr', attrs={'class': 'row1'})

    for stat in all_stats:
        each_stat = stat.find_all('td')
        print(each_stat)
        score = score_breakout(each_stat[2].text)
        game_exists = Game.query.filter_by(team=player.team,
                                           game_date=each_stat[0].text,
                                           opponent=each_stat[1].text,
                                           your_score=score[0],
                                           opponent_score=score[1]).first()
        if not game_exists:
            game_stats = Game(team=player.team,
                              game_date=each_stat[0].text,
                              opponent=each_stat[1].text,
                              your_score=score[0],
                              opponent_score=score[1])

            pass_stats = Passing(player_id=player.id,
                                 attempts=each_stat[3].text,
                                 completions=each_stat[4].text,
                                 yards=each_stat[6].text,
                                 touchdowns=each_stat[8].text)
            db.session.add(pass_stats)
            db.session.add(game_stats)
    db.session.commit()

def lookup_specific_stats(player_position):
    all_players = Player.query.filter_by(position=player_position)
    for player in all_players:
        quarterback_stat_lookup(player)

def score_breakout(score):
    scores = score.split('-')
    cleaned = [score.replace('W\xa0', '') for score in scores]
    return cleaned
