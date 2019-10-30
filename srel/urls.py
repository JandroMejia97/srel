from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import ObtainAuthToken

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('apps.reservas.urls', 'reservas'), namespace='reservas')),
    path('api/', include(('rest_framework.urls', 'rest_framework'), namespace='rest_framework')),
    path('api/auth', ObtainAuthToken.as_view())
]
