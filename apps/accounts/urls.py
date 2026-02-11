from django.urls import path

from .views import UserRegsiterView, UserLoginView, UserProfileView, ChangePasswordView


urlpatterns = [
    path('register/', UserRegsiterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change-password'),
]