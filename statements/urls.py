from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='statements'),
    path('order/', views.order, name='order'),
    # path('delplacereq/', views.del_place, name='delplace')
]