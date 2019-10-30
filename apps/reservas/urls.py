from django.urls import include, path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()
router.register(r'tipos', TipoCanchaViewSet)
router.register(r'canchas', CanchaViewSet)
router.register(r'reservas', ReservaViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
