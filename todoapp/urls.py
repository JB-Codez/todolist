from django.urls import path
from . import views

# refactor/src:  https://youtu.be/CA5duCGDSUE
# src: https://docs.djangoproject.com/en/4.2/howto/static-files/
from django.conf import settings
from django.conf.urls.static import static


app_name = 'todoapp' # giving this URLs.py an app name means that
                     # refering to it in html needs to precede it.
"""
w/o app_name:
    <form action="{% url 'edit_django_name' todoitem.id %}">
w/ app name:    
app_name = 'todoapp'
    <form action="{% url 'todoapp:edit_django_name' todoitem.id %}">
    
"""

urlpatterns = [
    path("", views.index_todoapp, name="to_do_django_name"),
    path("home",views.index_todoapp, name="to_do_django_name"),
    path("edit/<int:task_id>/", views.editTask, name="edit_django_name"),
    path("delete/<int:task_id>/", views.deleteTask, name="delete_django_name"),
   
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this is a helper function
# and only works in debug mode and should be discarded during production
# src: https://docs.djangoproject.com/en/4.2/howto/static-files/
# 1 implementation of this and the above x2 Import statements
