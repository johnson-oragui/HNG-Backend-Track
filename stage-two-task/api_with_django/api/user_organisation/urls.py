from django.urls import path
from user_organisation.views import get_organisation, get_organisations, add_user


urlpatterns = [
    path('api/organisations', get_organisations, name="get_organisations"),
    path('api/organisations/<str:orgId>', get_organisation, name="get_organisation"),
    path('api/organisations/<str:orgId>/users', add_user, name='add_user'),
]
