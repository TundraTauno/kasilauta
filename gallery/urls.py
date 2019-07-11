from django.urls import path
from . import views

# For static files.
from django.conf import settings
from django.conf.urls.static import static

# Create your urls here.
urlpatterns = [
        path('', views.index, name='index'),
        path('thread/<int:id>', views.thread, name='thread'),
        ]

# Static media files for test environment. Not suitable for production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
