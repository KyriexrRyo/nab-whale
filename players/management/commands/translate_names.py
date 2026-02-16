import time
from django.core.management.base import BaseCommand
from players.models import Player
from deep_translator import GoogleTranslator

class Command(BaseCommand):
    help = '英語のままの選手名を自動で日本語（カタカナ）に翻訳します'

    def handle(self, *args, **options):
        # 翻訳機をセットアップ
        translator = GoogleTranslator(source='en', target='ja')
        
        # 「日本語名」と「英語名」が全く同じ（＝まだ翻訳されていない）選手を探す
        # ※ update_statsで最初は同じ名前を入れているため
        players = Player.objects.all()
        
        count = 0
        total = players.count()
        
        self.stdout.write(f"全{total}選手の翻訳チェックを開始します...")

        for i, player in enumerate(players):
            # すでにカタカナになっている（英語名と違う）場合はスキップ
            if player.name_jp != player.name_en and player.name_jp != "":
                continue

            try:
                # 翻訳実行 (例: "LeBron James" -> "レブロン・ジェームズ")
                translated_text = translator.translate(player.name_en)
                
                # 翻訳結果を保存
                player.name_jp = translated_text
                player.save()
                
                count += 1
                self.stdout.write(f"[{count}] 翻訳: {player.name_en} -> {translated_text}")
                
                # Googleに怒られないように少し休憩
                time.sleep(0.5)

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"エラー ({player.name_en}): {e}"))

        self.stdout.write(self.style.SUCCESS(f'完了！ {count}人の名前を日本語化しました。'))