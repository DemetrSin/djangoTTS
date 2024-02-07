from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path

from users.views import index_redirect

# Your non-internationalized URL patterns here
non_i18n_urlpatterns = [
    path('admin/', admin.site.urls),
    path('tts/', include('tts.urls')),
    path('users/', include('users.urls')),
    path('', index_redirect)
]

urlpatterns = i18n_patterns(
    *non_i18n_urlpatterns,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
