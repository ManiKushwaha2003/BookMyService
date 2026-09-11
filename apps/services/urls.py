from django.urls import path
from .views import ServiceAPIView,ServiceByIdView


urlpatterns = [
    path("service/", ServiceAPIView.as_view(), name="service"),
    path("service/<int:id>", ServiceByIdView.as_view(), name="service_by_id")
]