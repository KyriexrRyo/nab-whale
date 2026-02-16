from django.shortcuts import render, get_object_or_404
from django.db.models import Q  # ← 検索用の道具を追加！
from .models import Player

# 一覧を表示（検索機能付き！）
def player_list(request):
    query = request.GET.get('q')  # 検索窓に入力された言葉を受け取る

    if query:
        # 言葉がある場合：名前(日/英)、バッシュ、ブランド、ウラNBAから探す
        # icontains = 大文字小文字を気にせず「含む」ものを探す
        players = Player.objects.filter(
            Q(name_en__icontains=query) |
            Q(name_jp__icontains=query) |
            Q(shoe_model__icontains=query) |
            Q(fashion_brands__icontains=query) |
            Q(ura_nba__icontains=query)
        ).order_by('team__name', 'name_en')
    else:
        # 言葉がない場合：全員を表示（今まで通り）
        players = Player.objects.all().order_by('team__name', 'name_en')

    # 'query': query を追加して、検索ワードを画面に戻してあげる（検索窓に残すため）
    return render(request, 'players/player_list.html', {'players': players, 'query': query})

# 詳細を表示（ここは変更なし）
def player_detail(request, pk):
    player = get_object_or_404(Player, pk=pk)
    return render(request, 'players/player_detail.html', {'player': player})