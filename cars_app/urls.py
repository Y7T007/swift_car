from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_car, name='add_car'),
    path('remove/<int:car_id>', views.remove_car, name='remove_car'),
    path('view-all', views.view_all_cars, name='view_all_cars'),
    path('view/<str:car_id>', views.view_car, name='view_car'),
    path('update/<int:car_id>', views.update_car, name='update_car'),
]