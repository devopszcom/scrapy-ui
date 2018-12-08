from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add-node', views.add_node, name='add_node'),
    path('nodes/<int:node_id>/<str:project_name>/status', views.status_node, name='status_node'),
    path('nodes/<int:node_id>/<str:project_name>/add-jobs/<str:spider_name>', views.add_job, name='add_job'),
    path('nodes/<int:node_id>/<str:project_name>/cancel-jobs/<str:job_id>', views.cancel_job, name='cancel_job'),
]
