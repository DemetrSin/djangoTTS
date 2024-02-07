from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),
    path('home', views.HomeView.as_view(), name='home'),
    path('profile/<int:pk>', login_required(views.UserProfileView.as_view()), name='profile'),
    path('profile/edit', login_required(views.EditProfileView.as_view()), name='edit_profile'),

]
