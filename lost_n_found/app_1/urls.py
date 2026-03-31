from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    
    path('', views.index, name='index'),
    path('login/', views.login_page, name='login'),
    path('map/', views.map_page, name='map'),
    path('newpost/', views.newpost_page, name='newpost'),
    path('msg/', views.msg_page, name='msg'),
    path('user/', views.user_page, name='user'),
    path('create/', views.create_page, name='create'),
    
    
    path('api/register/', views.register_user, name='register'),
    path('api/login/', views.login_user, name='api_login'),
    path('api/users/<int:user_id>/', views.get_user_profile, name='user_profile'),
    path('api/users/<int:user_id>/update/', views.update_user_profile, name='update_user'),
    path('api/users/<int:user_id>/posts/', views.get_user_posts, name='user_posts'),
    path('api/upload-profile-pic/', views.upload_profile_pic, name='upload_profile'),
    path('api/posts/', views.post_list, name='post_list'),
    path('api/posts/<int:post_id>/', views.delete_post, name='delete_post'),
    path('api/categories/', views.category_list, name='category_list'),
    path('api/messages/', views.send_message, name='send_message'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)