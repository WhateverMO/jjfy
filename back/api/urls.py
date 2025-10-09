from django.urls import path

from . import views

urlpatterns = [
    path("get_table_names", views.get_table_names),
    path("get_table", views.get_table),
    path("get_view_names", views.get_view_names),
    path("get_all_relations", views.get_all_relations),
    path("er", views.er),
    path("eval", views.eval),
]
