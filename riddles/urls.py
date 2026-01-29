from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('play/', views.riddle_game, name='riddle_game'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]