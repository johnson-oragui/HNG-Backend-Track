from django.urls import path
from user.views import get_user

urlpatterns = [
    path('api/users/<str:id>', get_user, name='get_user'),
]
