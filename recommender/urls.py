from django.urls import path, include
from . import views

app_name = 'recommender'

urlpatterns = [
    path('home/', views.home, name='home'),
    path("",views.showslides),
    path('about/', views.about, name='about'),
    path('team/', views.about_team, name='team'),
    path('best/', views.searchform_get, name='best'),
    path('bestp/', views.searchform_post, name='bestp'),
    path('bestuser/', views.user_searchform_get, name='bestuser'),
    path('bestuserp/', views.user_searchform_post, name='bestuserp'),
    path('playlist/', views.playlist_get, name='playlist'),
    path('playlistb/', views.playlist_post, name='playlistb'),
    path('playlistaddb/<str:songid>/', views.playlistadd_post, name='playlistaddb'),
    path('playlist/<str:playlistid>/<str:songid>/', views.playlistadd_get, name='playlistadd'),
    path('playlistdelete/<str:playlistid>/<str:songid>/', views.playlistdeletesong, name='playlistdeletesong'),
    path('playlistdelete/<str:playlistid>/', views.playlistdelete, name='playlistdelete'),
    path('playlistpublic/<str:playlistid>/<str:public>', views.playlistpublic, name='playlistpublic'),
    path('bestuserp/<str:username>/', views.user_info, name='userinfo'),
    path('friendrequests', views.friend_request, name='friend_requests'),
    path('likes/<str:id>/<str:add>', views.like_list, name='like_list'),
    path('playlistlikes/<str:id>/<str:add>', views.playlistlike_list, name='playlistlike_list'),
    path('playlistlikesdelete/<str:id>', views.playlistlikedelete_list, name='playlistlikedelete_list'),
    path('likes/', views.profilelikes, name='likes'),
    path('searchbysong/', views.searchbysong_get, name='searchbysong'),
    path('searchbysongp/', views.searchbysong_post, name='searchbysongp')
    ]