import requests
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from players.models import Player, Team
from nba_api.stats.endpoints import leaguedashplayerstats

class Command(BaseCommand):
    help = '全NBA選手を自動取得・更新し、画像もダウンロードします'

    def handle(self, *args, **options):
        target_season = '2025-26'
        self.stdout.write(f"NBA.comから {target_season} のデータを取得中...")

        try:
            # データ取得
            stats = leaguedashplayerstats.LeagueDashPlayerStats(
                season=target_season, 
                per_mode_detailed='PerGame'
            )
            data = stats.get_dict()
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"データ取得エラー: {e}"))
            return
        
        # データを扱いやすいリストに変換
        result_sets = data['resultSets'][0]
        headers = result_sets['headers']
        row_set = result_sets['rowSet']
        players_data = [dict(zip(headers, row)) for row in row_set]

        count_new = 0
        count_update = 0
        count_img = 0
        
        total = len(players_data)
        self.stdout.write(f"全{total}選手の処理を開始します...")

        for i, p_data in enumerate(players_data):
            api_name = p_data['PLAYER_NAME']
            team_abbr = p_data['TEAM_ABBREVIATION']
            player_id = p_data['PLAYER_ID'] # IDを取得（重要！）
            
            if not team_abbr:
                continue
                
            # チーム取得or作成
            team_obj, _ = Team.objects.get_or_create(name=team_abbr)

            # 選手取得
            player = Player.objects.filter(name_en=api_name).first()

            if player:
                # 既存選手の更新
                player.team = team_obj
                player.ppg = p_data['PTS']
                player.rpg = p_data['REB']
                player.apg = p_data['AST']
                # ※ここでsave()はまだしない（画像処理の後でまとめて保存）
                count_update += 1
            else:
                # 新規作成
                player = Player(
                    name_en=api_name,
                    name_jp=api_name,
                    team=team_obj,
                    ppg=p_data['PTS'],
                    rpg=p_data['REB'],
                    apg=p_data['AST']
                )
                count_new += 1

            # --- 画像ダウンロード処理 ---
            # まだ画像がない場合のみ実行（毎回やると遅いので）
            if not player.image:
                # NBA公式の画像URLパターン
                img_url = f"https://ak-static.cms.nba.com/wp-content/uploads/headshots/nba/latest/260x190/{player_id}.png"
                
                try:
                    response = requests.get(img_url, timeout=5)
                    if response.status_code == 200:
                        # ファイル名を決定（例: LeBron James.png）
                        file_name = f"{api_name}.png"
                        # 画像フィールドにバイナリデータを保存
                        player.image.save(file_name, ContentFile(response.content), save=False)
                        count_img += 1
                        self.stdout.write(f"  [画像GET] {api_name}")
                except Exception as e:
                    self.stdout.write(f"  [画像失敗] {api_name}: {e}")

            # 最後にまとめて保存
            player.save()

            # 進捗表示（50人ごと）
            if (i + 1) % 50 == 0:
                self.stdout.write(f"  ... {i + 1}/{total} 完了")

        self.stdout.write(self.style.SUCCESS(f'完了！ 新規: {count_new} / 更新: {count_update} / 画像DL: {count_img}'))