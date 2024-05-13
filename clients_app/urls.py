from django.urls import path
from . import views

urlpatterns = [
    path('view/<str:client_id>', views.view_client, name='view_client'),
    path('add', views.add_client, name='add_client'),
    path('view-all', views.view_all_clients, name='view_all_clients'),
    path('update/<str:client_id>', views.update_client, name='update_client'),
]