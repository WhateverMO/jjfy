from django.urls import path

from . import views

urlpatterns = [
    path("testHTML", views.testHMTL),
    path("get_table_names", views.get_table_names),
    path("get_table", views.get_table),
    path("get_view_names", views.get_view_names),
    path("get_all_relations", views.get_all_relations),
    path("er", views.er),
    path("erfit", views.erfit),
    path("api1", views.api1),
    path("http1", views.http1),
    path("api2", views.api2),
    path("http2", views.http2),
]
