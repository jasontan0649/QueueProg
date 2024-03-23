from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('current/', views.current_number, name='current_number'),
    path('new/', views.new_number, name='new_number'),
    path('admin_next/', views.admin_next, name='admin_next'),
    path('number/<int:number>/', views.number_detail, name='number_detail'), 
]
