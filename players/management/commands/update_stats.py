from django.core.management.base import BaseCommand
from players.models import Player
from nba_api.stats.endpoints import leaguedashplayerstats

class Command(BaseCommand):
    help = 'NBA公式サイトから最新スタッツを取得し、英語名が一致する選手を更新します'

    def handle(self, *args, **options):
        self.stdout.write("NBA.comからデータを取得中...")

        # 最新シーズンのデータを取得 (必要に応じて '2025-26' などに変更)
        stats = leaguedashplayerstats.LeagueDashPlayerStats(season='2024-25')
        data = stats.get_dict()
        
        # APIの結果からリストとヘッダーを取り出す
        result_sets = data['resultSets'][0]
        headers = result_sets['headers']
        row_set = result_sets['rowSet']

        # データを扱いやすくするための辞書リストを作成
        players_data = []
        for row in row_set:
            player_dict = dict(zip(headers, row))
            players_data.append(player_dict)

        updated_count = 0
        
        # 取得した全NBA選手データをループ
        for p_data in players_data:
            api_name = p_data['PLAYER_NAME'] # 例: "Rui Hachimura"
            
            # 自分のDBに「同じ英語名」の選手がいるか探す
            try:
                # name_en が一致する選手を取得
                player = Player.objects.get(name_en=api_name)
                
                # 数値を更新
                player.ppg = p_data['PTS']  # 平均得点
                player.rpg = p_data['REB']  # 平均リバウンド
                player.apg = p_data['AST']  # 平均アシスト
                
                player.save()
                self.stdout.write(f"更新: {player.name_jp} ({player.ppg} PPG)")
                updated_count += 1
                
            except Player.DoesNotExist:
                # DBにいない選手は無視する（全NBA選手を登録したいわけではないため）
                continue
            except Player.MultipleObjectsReturned:
                self.stdout.write(self.style.WARNING(f"重複エラー: {api_name} がDBに複数います"))
                continue

        self.stdout.write(self.style.SUCCESS(f'完了！ {updated_count} 人のデータを更新しました。'))