from django.urls import path
from . import views

urlpatterns = [
    path('new', views.new_reservation, name='new_reservation'),
    path('view-all', views.view_all_reservations, name='view_all_reservations'),
    path('view/<int:reservation_id>', views.view_reservation, name='view_reservation'),
]