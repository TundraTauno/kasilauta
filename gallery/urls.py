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
        path('create_thread/<slug:board>', views.create_thread, name='create_thread'),
        path('create_post/<slug:board>/<int:thread>', views.create_post, name='create_post'),
        # user actions on post
        path('user_action/<slug:board>/<int:thread>/<int:post>', views.user_action, name='user_action'),
        ]

# Static media files for test environment. Not suitable for production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
