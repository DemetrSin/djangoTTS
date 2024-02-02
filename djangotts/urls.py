from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from users.views import index_redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tts/', include('tts.urls')),
    path('users/', include('users.urls')),
    path('', index_redirect)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)