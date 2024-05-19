from django.urls import path
from . import views

urlpatterns = [
    path('add', views.new_reservation, name='new_reservation'),
    path('view-all', views.view_all_reservations, name='view_all_reservations'),
    path('view/<int:reservation_id>', views.view_reservation, name='view_reservation'),
    path('sum-prices-per-month', views.sum_prices_per_month, name='sum_prices_per_month'),
    path('sum-prices-by-week', views.sum_prices_by_week, name='sum_prices_by_week'),
    path('reservations-per-day', views.reservations_per_day, name='reservations_per_day'),
    path('reservations-by-manager', views.reservations_by_manager, name='reservations_by_manager'),
]