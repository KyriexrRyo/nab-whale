from django.core.management.base import BaseCommand
from players.models import Player, Team
from nba_api.stats.endpoints import leaguedashplayerstats

class Command(BaseCommand):
    help = '全NBA選手を自動取得・登録・更新します（2025-26シーズン）'

    def handle(self, *args, **options):
        # 設定に合わせて 2025-26 シーズンを指定
        target_season = '2025-26'
        
        self.stdout.write(f"NBA.comから {target_season} シーズンの全データを取得中...")

        try:
            # 指定シーズンの平均スタッツを取得
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=target_season, 
                per_mode_detailed='PerGame'
            )
            data = stats.get_dict()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"エラー: データの取得に失敗しました。\n詳細: {e}"))
            return
        
        # データをリスト化
        result_sets = data['resultSets'][0]
        headers = result_sets['headers']
        row_set = result_sets['rowSet']

        players_data = []
        for row in row_set:
            players_data.append(dict(zip(headers, row)))

        count_new = 0
        count_update = 0
        
        # 全選手をループ処理
        for p_data in players_data:
            api_name = p_data['PLAYER_NAME']        # 例: LeBron James
            team_abbr = p_data['TEAM_ABBREVIATION'] # 例: LAL
            
            # 1. チームの処理（なければ作る）
            if not team_abbr:
                continue
                
            team_obj, created = Team.objects.get_or_create(name=team_abbr)

            # 2. 選手の処理
            # update_or_create だと条件分岐が複雑になるため、
            # 「検索して存在確認」→「あれば更新、なければ作成」という確実な手順にします。
            
            player = Player.objects.filter(name_en=api_name).first()

            if player:
                # --- A. 既存選手の更新 ---
                # 日本語名(name_jp)は変更せず、スタッツとチームだけ更新する
                player.team = team_obj
                player.ppg = p_data['PTS']
                player.rpg = p_data['REB']
                player.apg = p_data['AST']
                player.save()
                count_update += 1
            else:
                # --- B. 新規選手の作成 ---
                # 日本語名にはとりあえず英語名を入れておく
                Player.objects.create(
                    name_en=api_name,
                    name_jp=api_name, # 初期値は英語名
                    team=team_obj,
                    ppg=p_data['PTS'],
                    rpg=p_data['REB'],
                    apg=p_data['AST']
                )
                self.stdout.write(f"新規登録: {api_name}")
                count_new += 1

        self.stdout.write(self.style.SUCCESS(f'完了！ 新規登録: {count_new}人 / 更新: {count_update}人'))