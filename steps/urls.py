from django.urls import path
from steps import views

urlpatterns = [
    path('create/', views.StepCreateView.as_view(), name='action-create'),
    path('', views.StepListView.as_view(), name='action-list'),
    path('<int:pk>/', views.StepDetailView.as_view(), name='action-detail'),
    path('<int:pk>/update', views.StepUpdateView.as_view(), name='action-update'),
    path('<int:pk>/deactivate/', views.StepDeactivateView.as_view(), name='action-deactivate'),
]