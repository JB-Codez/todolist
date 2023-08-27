from django.contrib import admin

# Register your models here.
from .models import ToDoItem

class ToDoItemAdmin(admin.ModelAdmin):
    readonly_fields = ['id',]
    raw_id_fields=['task_author',]

admin.site.register(ToDoItem,ToDoItemAdmin)