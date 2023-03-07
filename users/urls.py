from django.urls import path, include
from users import views

urlpatterns = [
    path('', views.EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('<int:pk>/deactivate/', views.EmployeeDeactivateView.as_view(), name='employee-deactivate'),
]