from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='home'),
    path('connect_ystu/', views.ystu_connect, name='ystu_connect'),
    path('sw.js',
         views.ServiceWorkerView.as_view(),
         name='sw',
         ),
    path('registration/', views.registration, name='registration'),
    path('registration/register/', views.create_account, name='register'),
]

