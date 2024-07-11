from django.urls import path
from authentication.views import register_user, login_user

urlpatterns = [
    path('api/auth/register', register_user, name='register_user'),
    path('api/auth/login', login_user, name='login_user'),
]
