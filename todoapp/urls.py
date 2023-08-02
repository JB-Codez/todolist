from django.urls import path
from . import views

urlpatterns = [
    path("", views.index_todoapp, name="to_do_django_name"),
    path("edit/<int:task_id>/", views.editTask, name="edit_django_name"),
    path("delete/<int:task_id>/", views.deleteTask, name="delete_django_name",)
]
