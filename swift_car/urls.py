from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('auth/', include('auth_app.urls')),
    path('dashboard/', include('dashboard_app.urls')),
    path('cars/', include('cars_app.urls')),
    path('reservations/', include('reservations_app.urls')),
    path('clients/', include('clients_app.urls')),
    path('managers/', include('managers_app.urls')),
    path('agencies/', include('agencies_app.urls')),

]