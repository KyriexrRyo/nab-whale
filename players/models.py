from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=100)
    color_primary = models.CharField(max_length=7, default='#333333')   # メインカラー
    color_secondary = models.CharField(max_length=7, default='#888888') # サブカラー

    def __str__(self):
        return self.name

class Player(models.Model):
    # --- 基本情報 ---
    name_en = models.CharField("英語名", max_length=100) # API連携に必須
    name_jp = models.CharField("日本語名", max_length=100)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="所属チーム")
    image = models.ImageField("選手画像", upload_to='player_images/', blank=True, null=True)

    # --- スタッツ (APIで自動更新) ---
    ppg = models.FloatField("平均得点", default=0.0)
    rpg = models.FloatField("平均リバウンド", default=0.0)
    apg = models.FloatField("平均アシスト", default=0.0)

    # --- 選手をもっと好きになる情報 (リクエストの6項目) ---
    # 1. バッシュ
    shoe_model = models.CharField("着用バッシュ", max_length=100, blank=True, null=True)
    
    # 2. ブランド
    fashion_brands = models.TextField("よく着ているブランド", blank=True, null=True)
    
    # 3. Instagram (IDではなくURLの方が便利です)
    instagram = models.URLField("Instagram URL", blank=True, null=True)
    
    # 4. YouTube
    youtube = models.URLField("YouTube URL", blank=True, null=True)
    
    # 5. ポッドキャスト
    podcast = models.URLField("ポッドキャスト URL", blank=True, null=True)

    # 6. ウラNBA
    ura_nba = models.TextField("ウラNBA（豆知識）", blank=True, null=True)

    def __str__(self):
        return self.name_en
    # --- ↓↓↓ 一番下に追加してください ↓↓↓ ---

class TunnelFit(models.Model):
    # どの選手に紐づくか？
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fits')
    
    # 画像ファイル
    image = models.ImageField("ギャラリー画像", upload_to='gallery/')
    
    # ちょっとしたメモ（例: 2024開幕戦）
    caption = models.CharField("キャプション", max_length=200, blank=True)

    def __str__(self):
        return f"{self.player.name_jp}の画像"