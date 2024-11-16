from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='schedule'),
    path('getSchedule/', views.get_schedule)
]