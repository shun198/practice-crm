from django.urls import path

from application.views.health_check import health_check

urlpatterns = [
    path(r"health/", health_check, name="health_check"),
]
