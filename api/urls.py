from django.urls import path

from . import views

urlpatterns = [
    path("api1", views.api1),
    path("http1", views.http1),
    path("api2", views.api2),
    path("http2", views.http2),
]
