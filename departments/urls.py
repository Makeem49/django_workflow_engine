from django.urls import path, include
from departments import views

urlpatterns = [
    path('', views.DepartmentListCreateView.as_view(), name='department-list-create'),
    path('<int:pk>/', views.DepartmentDetail.as_view(), name='department-detail'),
    path('<int:pk>/deactivate/', views.DepartmentDeactivateView.as_view(), name='department-delete'),
]