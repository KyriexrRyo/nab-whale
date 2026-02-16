from django.contrib import admin
from .models import Player, Team, TunnelFit # ← TunnelFitを追加！

# 選手の編集画面の中に、ギャラリー追加欄を作る設定
class TunnelFitInline(admin.TabularInline):
    model = TunnelFit
    extra = 1 # 最初から1つ空欄を表示しておく

class PlayerAdmin(admin.ModelAdmin):
    # 一覧画面で見たい項目
    list_display = ('name_jp', 'name_en', 'team', 'shoe_model', 'instagram')
    list_filter = ('team',)
    search_fields = ('name_jp', 'name_en', 'shoe_model', 'fashion_brands', 'ura_nba')
    
    # ここでギャラリー機能を合体！
    inlines = [TunnelFitInline]

    fieldsets = (
        ('基本情報', {'fields': ('name_jp', 'name_en', 'team', 'image')}),
        ('スタッツ', {'fields': ('ppg', 'rpg', 'apg')}),
        ('Deep Dive', {'fields': ('shoe_model', 'fashion_brands', 'ura_nba')}),
        ('メディア・SNS', {'fields': ('instagram', 'youtube', 'podcast')}),
    )

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'color_primary', 'color_secondary')

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)