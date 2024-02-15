from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('login', views.login, name='login'),
    path('callback', views.callback, name='callback'),
    path('logout', views.logout, name='logout'),
    path('home', views.HomeView.as_view(), name='home'),
    path('profile/<int:pk>', views.UserProfileView.as_view(), name='profile'),
    path('profile/edit/', views.EditProfileView.as_view(), name='edit_profile'),
    path('subscription', views.SubscriptionView.as_view(), name='subscription')
]
