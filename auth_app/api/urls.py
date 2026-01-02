from django.urls import path
from .views import RegisterView, LoginView, RefreshToken, LogoutView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', RefreshToken.as_view(), name='refresh_token'),
    path('logout/', LogoutView.as_view(), name='logout')
]