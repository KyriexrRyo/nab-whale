from django.contrib import admin
from .models import Player, Team, TunnelFit

# 画像をインライン（埋め込み）で表示する設定
class TunnelFitInline(admin.TabularInline):
    model = TunnelFit
    extra = 1  # 最初から空欄を1つ出しておく

# 選手の管理画面設定
class PlayerAdmin(admin.ModelAdmin):
    inlines = [TunnelFitInline]  # ここで合体！

# 登録
admin.site.register(Player, PlayerAdmin)
admin.site.register(Team)