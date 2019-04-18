from django.conf.urls import url
from django.urls import path
from manage_team import views

app_name = 'manage_team'

urlpatterns = [
    path('',views.index,name='index'),
    path('player_registration',views.player_registration,name='/player_registration'),
    path('create_game',views.create_game,name='/create_game'),
    path('create_team',views.create_team,name='/create_team'),
    path('team_decider',views.team_decider,name='/team_decider'),
    path('player_info',views.player_info, name = 'player_info'),
    path('game_info',views.game_info, name = 'game_info'),
    path('team_info',views.team_info, name = 'team_info'),
    path('point_decider',views.point_decider, name = 'point_decider'),
    path('team_game_info',views.team_game_info, name = 'team_game_info'),
    path('player_game_info',views.player_game_info, name = 'player_game_info'),
    path('leaderboard',views.leaderboard, name = 'leaderboard')
]