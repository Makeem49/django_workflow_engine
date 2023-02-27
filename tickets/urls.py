from django.urls import path

from tickets import views


urlpatterns = [
    path('create', views.TicketCreateView.as_view(), name='ticket-create'),
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-details'),
    path('<int:pk>/update', views.TicketUpdateView.as_view(), name='ticket-update'),
    path('<int:pk>/decide/', views.TicketDecisionView.as_view(), name='ticket-decide'),
    path('owner/', views.OwnerTicketView.as_view(), name='ticket-owner'),
    path('<int:pk>/delete', views.TicketDeleteView.as_view(), name='ticket-owner'),
    # path('<int:pk>/delete', views.TicketDeleteView.as_view(), name='ticket-owner'),

]
