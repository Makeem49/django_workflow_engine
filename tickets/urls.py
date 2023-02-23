from django.urls import path

from tickets import views


urlpatterns = [
    path('create', views.TicketCreateView.as_view(), name='ticket-create'),
    path('', views.TicketListView.as_view(), name='ticket-list'),
    path('<int:pk>/', views.TicketDetail.as_view(), name='ticket-detail')
]