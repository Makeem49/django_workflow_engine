from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from tickets import views


urlpatterns = [
    path('', obtain_auth_token),
]