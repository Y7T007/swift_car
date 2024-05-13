from django.urls import path
from . import views

urlpatterns = [
    path('view/<str:agency_id>', views.view_agency, name='view_agency'),
    path('add', views.add_agency, name='add_agency'),
    path('view-all', views.view_all_agencys, name='view_all_agencys'),
    path('update/<str:agency_id>', views.update_agency, name='update_agency'),
]