from django.core.management.base import BaseCommand
from players.models import Team

class Command(BaseCommand):
    help = 'NBA全チームのカラーを設定します'

    def handle(self, *args, **options):
        # チーム名(略称): [メインカラー, サブカラー]
        nba_colors = {
            'ATL': ['#E03A3E', '#C1D32F'], 'BOS': ['#007A33', '#BA9653'],
            'BKN': ['#000000', '#FFFFFF'], 'CHA': ['#1D1160', '#00788C'],
            'CHI': ['#CE1141', '#000000'], 'CLE': ['#860038', '#041E42'],
            'DAL': ['#00538C', '#B8C4CA'], 'DEN': ['#0E2240', '#FEC524'],
            'DET': ['#C8102E', '#1D42BA'], 'GSW': ['#1D428A', '#FFC72C'],
            'HOU': ['#CE1141', '#000000'], 'IND': ['#002D62', '#FDBB30'],
            'LAC': ['#C8102E', '#1D428A'], 'LAL': ['#552583', '#FDB927'],
            'MEM': ['#5D76A9', '#12173F'], 'MIA': ['#98002E', '#F9A01B'],
            'MIL': ['#00471B', '#EEE1C6'], 'MIN': ['#0C2340', '#236192'],
            'NOP': ['#0C2340', '#85714D'], 'NYK': ['#006BB6', '#F58426'],
            'OKC': ['#007AC1', '#EF3B24'], 'ORL': ['#0077C0', '#C4CED4'],
            'PHI': ['#006BB6', '#ED174C'], 'PHX': ['#1D1160', '#E56020'],
            'POR': ['#E03A3E', '#000000'], 'SAC': ['#5A2D81', '#63727A'],
            'SAS': ['#C4CED4', '#000000'], 'TOR': ['#CE1141', '#000000'],
            'UTA': ['#002B5C', '#00471B'], 'WAS': ['#002B5C', '#E31837'],
        }

        count = 0
        for team_name, colors in nba_colors.items():
            # チームが存在するか確認してから色をセット
            team = Team.objects.filter(name=team_name).first()
            if team:
                team.color_primary = colors[0]
                team.color_secondary = colors[1]
                team.save()
                count += 1
                self.stdout.write(f"設定: {team_name}")

        self.stdout.write(self.style.SUCCESS(f'完了！ {count}チームの色を設定しました。'))