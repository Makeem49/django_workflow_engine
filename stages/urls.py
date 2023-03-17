from django.urls import path
from stage import views

urlpatterns = [
    path('create/', views.StageCreateView.as_view(), name='stage-create'),
    path('', views.StageListView.as_view(), name='stage-list'),
    path('<int:pk>/', views.StageDetailView.as_view(), name='stage-detail'),
    path('<int:pk>/update', views.StageUpdateView.as_view(), name='stage-update'),
    path('<int:pk>/deactivate/', views.StageDeactivateView.as_view(), name='stage-deactivate'),
]