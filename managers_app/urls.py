from django.urls import path
from . import views

urlpatterns = [
    path('view-all', views.view_all_managers, name='view_all_managers'),
    path('view/<str:manager_id>', views.view_manager, name='view_manager'),
    path('add', views.add_manager, name='add_manager'),
    path('update', views.update_manager, name='update_manager'),
    path('remove/<int:manager_id>', views.remove_manager, name='remove_manager'),
]