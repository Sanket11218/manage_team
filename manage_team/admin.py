# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from manage_team.models import PlayerInfo,GameInfo,TeamInfo

# Register your models here.

admin.site.register(PlayerInfo)
admin.site.register(GameInfo)
admin.site.register(TeamInfo)
