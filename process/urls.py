from django.urls import path
from process import views

urlpatterns = [
    path('create/', views.ProcessCreateView.as_view(), name='process-create'),
    path('', views.ProcessListView.as_view(), name='process-list'),
    path('<int:pk>/', views.ProcessDetailView.as_view(), name='process-detail'),
    path('<int:pk>/update', views.ProcessUpdateView.as_view(), name='process-update'),
    path('<int:pk>/deactivate/', views.ProcessDeactivateView.as_view(), name='process-deactivate'),
]