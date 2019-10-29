from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.reservas.urls', 'reservas'), namespace='reservas')),
    path('api/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework'))
]
