import http.client
from bs4 import BeautifulSoup
from .models import Player, Passing, Game, Rushing
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


def initial_player_lookup(position='qb'):
    position_url = {'qb':'PTDS', 'rb':'RYDS', 'wr':'RECTDS'}
    position_path = 'stats/leaders/NCAAF/' + position_url[position] + \
                                            '/regularseason?&start_row=1'
    souped_page = url_request(position_path)
    all_players = souped_page.find_all('tr', attrs={'class': 'row2'})
    all_players.extend(souped_page.find_all('tr', attrs={'class': 'row1'}))
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






def quarterback_stat_lookup(player):
    print('player', player.name)
    player_name = player.name.replace('.', '')
    player_name = player_name.replace(' ', '-')
    print('player name', player_name)
    souped_page = url_request('players/playerpage/' + str(player.ext_id) + '/' + player_name)
    souped_page = souped_page.find('table', attrs={'class': 'borderTop'})
    all_stats = souped_page.find_all('tr', attrs={'class': 'row1'})
    all_stats.extend(souped_page.find_all('tr', attrs={'class': 'row2'}))

    for stat in all_stats[1:]:
        each_stat = stat.find_all('td')
        score = score_breakout(each_stat[2].text)
        game_obj, created = Game.objects.get_or_create(team=player.team,
                                                       game_date=each_stat[0].text,
                                                       opponent=each_stat[1].text,
                                                       your_score=score[0],
                                                       opponent_score=score[1])
        if created:
            pass_stats = Passing(player_id=player,
                                 attempts=each_stat[3].text,
                                 completions=each_stat[4].text,
                                 yards=each_stat[6].text,
                                 touchdowns=each_stat[8].text,
                                 interceptions=each_stat[9].text)

            rush_stats = Rushing(player_id=player,
                                 attempts=each_stat[10].text,
                                 yards=each_stat[11].text,
                                 touchdowns=each_stat[13].text)
            pass_stats.save()
            rush_stats.save()

def lookup_specific_stats(player_position):
    all_players = Player.objects.filter(position=player_position)
    for player in all_players:
        quarterback_stat_lookup(player)

def score_breakout(score):
    return re.findall(r'\d+', score)










#Not using
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
