from django.urls import path
from . import views

urlpatterns = [
    # 一覧ページ
    path('', views.player_list, name='player_list'),
    
    # 詳細ページ（<int:pk> は "ここに数字が入るよ" という意味です）
    path('player/<int:pk>/', views.player_detail, name='player_detail'),
]