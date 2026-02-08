from django.db import models

class Team(models.Model):
    name = models.CharField("チーム名", max_length=50)
    color_primary = models.CharField("メインカラー", max_length=7, default='#333333', help_text="HEXコード (例: #552583)")
    color_secondary = models.CharField("サブカラー", max_length=7, default='#eeeeee', help_text="HEXコード (例: #FDB927)")
    
    def __str__(self):
        return self.name

class Player(models.Model):
    name_jp = models.CharField("日本語名", max_length=100)
    instagram_id = models.CharField("Instagram ID", max_length=50, blank=True, help_text="例: rui_8mura")
    twitter_id = models.CharField("X (Twitter) ID", max_length=50, blank=True, help_text="例: rui_8mura")
    youtube_url = models.URLField("YouTube URL", blank=True, help_text="チャンネルのURL")
    # ↑↑↑ ここまで追加 ↑↑↑
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, verbose_name="所属チーム")
    image = models.ImageField("選手画像", upload_to='images/', blank=True, null=True)

    # ファッション・ギア
    current_shoe_model = models.CharField("着用バッシュ名", max_length=100, blank=True)
    fashion_style = models.CharField("私服の系統", max_length=100, blank=True)

    # パラメータ（5段階）
    param_fashion = models.IntegerField("オシャレ度", default=3)
    param_sns = models.IntegerField("SNS更新頻度", default=3)
    
    # 豆知識
    trivia = models.TextField("豆知識・裏話", blank=True)

    def __str__(self):
        return self.name_jp

# --- これまでのコードの下に追加 ---

class TunnelFit(models.Model):
    # どの選手に紐づくか？（related_name='fits' が合言葉になります）
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='fits')
    
    image = models.ImageField("ギャラリー画像", upload_to='gallery/')
    caption = models.CharField("キャプション", max_length=200, blank=True, help_text="例：2024開幕戦のセットアップ")

    def __str__(self):
        return f"{self.player.name_jp}の画像"