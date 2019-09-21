from django.urls import path
from . import views

# For static files.
from django.conf import settings
from django.conf.urls.static import static

# Create your urls here.
urlpatterns = [
        # index
        path('', views.index, name='index'),
        # board view 
        path('<slug:name>/', views.board_view, name='board_view'),
        # thread detail 
        path('<slug:name>/<int:id>', views.thread_detail, name='thread_detail'),
        # post form
        path('create_post/<slug:board>/<int:id>', views.create_post, name='create_post'),
        ]

# Static media files for test environment. Not suitable for production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
