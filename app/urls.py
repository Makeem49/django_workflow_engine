from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('employee/', include('users.urls')),
    path('ticket/', include('tickets.urls')),
    path('department/', include('departments.urls'))
]
