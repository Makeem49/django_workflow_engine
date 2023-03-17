from django.urls import path
from steps import views

urlpatterns = [
    path('create/', views.StepCreateView.as_view(), name='step-create'),
    path('', views.StepListView.as_view(), name='step-list'),
    path('<int:pk>/', views.StepDetailView.as_view(), name='step-detail'),
    path('<int:pk>/update', views.StepUpdateView.as_view(), name='step-update'),
    path('<int:pk>/deactivate/', views.StepDeactivateView.as_view(), name='step-deactivate'),
]