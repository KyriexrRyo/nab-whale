from django.contrib import admin
from django.urls import path, include
# ↓↓↓ この2行を追加！ ↓↓↓
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('players.urls')),
]

# ↓↓↓ これを追加！画像を表示するためのおまじない ↓↓↓
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)