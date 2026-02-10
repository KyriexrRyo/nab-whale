from django.shortcuts import render, get_object_or_404
from .models import Player

# 一覧を表示
def player_list(request):
    players = Player.objects.all().order_by('team__name', 'name_en')
    return render(request, 'players/player_list.html', {'players': players})

# 詳細を表示（pkはPrimary Key=IDのこと）
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'players/player_detail.html', {'player': player})