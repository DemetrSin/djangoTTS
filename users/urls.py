from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),
    path('home', views.HomeView.as_view(), name='home'),
    path('profile/<int:pk>',
         login_required(
             function=views.UserProfileView.as_view(),
             login_url='login'
         ),
         name='profile'),
    path('profile/edit/',
         login_required(
             function=views.EditProfileView.as_view(),
             login_url='login'
         ),
         name='edit_profile'),
    path('subscription',
         login_required(
             function=views.SubscriptionView.as_view(),
             login_url='login'
         ),
         name='subscription')
]
