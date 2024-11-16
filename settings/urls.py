from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='settings'),
    path('session/', views.sessions, name='session'),
    path('session/delete_session/', views.del_session, name='delete_session'),
    path('profile/', views.view_profile, name='profile_info'),
    path('profile/ystu_disconnect', views.ystu_disconnect, name='ystu_disconnect')
]