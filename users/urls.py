from django.urls import path, include
from users import views

urlpatterns = [
    path('department/', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('department/<int:pk>/', views.DepartmentDetail.as_view(), name='department-detail'),
    path('department/<int:pk>/deactivate/', views.DepartmentDeactivateView.as_view(), name='department-delete'),
    path('employee/', views.EmployeeListCreateView.as_view(), name='employee-create'),
    path('employee/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employee/<int:pk>/deactivate/', views.EmployeeDeactivateView.as_view(), name='employee-deactivate'),
]