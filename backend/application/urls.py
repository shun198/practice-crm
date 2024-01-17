from django.urls import include, path
from rest_framework_nested import routers

from application.views.customer import CustomerPhotoViewSet, CustomerViewSet
from application.views.health_check import health_check
from application.views.login import LoginViewSet
from application.views.product import ProductViewSet
from application.views.user import UserViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"", LoginViewSet, basename="login")
router.register(r"users", UserViewSet, basename="user")
router.register(r"customers", CustomerViewSet, basename="customer")
router.register(r"products", ProductViewSet, basename="product")
customer_router = routers.NestedDefaultRouter(
    router, "customers", lookup="customer"
)
customer_router.register(r"photos", CustomerPhotoViewSet, basename="photo")


urlpatterns = [
    path(r"", include(router.urls)),
    path(r"", include(customer_router.urls)),
    path(r"health/", health_check, name="health_check"),
]
