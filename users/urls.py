from django.urls import path, include
from .v import home 

urlpatterns = [
    path('/', home)
]