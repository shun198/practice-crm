from application.views.health_check import health_check
from application.views.login import LoginViewSet
from application.views.user import UserViewSet
from django.urls import include, path
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register(r"", LoginViewSet, basename="login")
router.register(r"users", UserViewSet, basename="user")

urlpatterns = [
    path(r"", include(router.urls)),
    path(r"health/", health_check, name="health_check"),
]