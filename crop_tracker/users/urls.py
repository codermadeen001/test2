from django.urls import path
from .views import login,create_agent, get_all_users

urlpatterns = [
    path('login/', login),
    path('register/', create_agent),
    path('all/', get_all_users),
]