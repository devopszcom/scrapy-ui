from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-node', views.add_node, name='add_node'),
    path('nodes/<int:node_id>/status', views.status_node, name='status_node'),
]
