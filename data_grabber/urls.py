from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.players, name='players'),
    url(r'^player/(?P<player_id>[0-9]+)/$', views.player_detail, name='player_detail'),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.game_detail, name='game_detail'),
    url(r'^predictions/$', views.predictions, name='predictions')
    ]
