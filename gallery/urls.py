from django.urls import path, register_converter
from . import url_matchers, views

# For static files.
from django.conf import settings
from django.conf.urls.static import static

register_converter(url_matchers.board_converter, 'board_slug')

# Create your urls here.
urlpatterns = [
        # index
        path('', views.index, name='index'),
        # board view 
        path('<board_slug:name>/', views.board_view, name='board_view'),
        # thread detail 
        path('<board_slug:name>/<int:id>', views.thread_detail, name='thread_detail'),
        # thread form
        path('create_thread/<board_slug:board>', views.create_thread, name='create_thread'),
        # post form
        path('create_post/<board_slug:board>/<int:thread>', views.create_post, name='create_post'),
        # user actions on post
        path('user_action/<board_slug:board>/<int:thread>/<int:post>', views.user_action, name='user_action'),
        ]

# Static media files for test environment. Not suitable for production.
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
