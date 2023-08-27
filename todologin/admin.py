from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError


from .forms import UserCreationForm, UserChangeForm
from .models import DashboardUser

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = DashboardUser
    #readonly_fields = ['id',]
    list_display = ["username","email",] # controls the columns on the Users admin row page
    fieldsets=[
        (
            None,
            {
                "fields" : [ "username","email", "user_image" ],
            },
        ),
        (
          "Personal Info",
          {
                "fields" : ["first_name", "last_name"],  
          },
        ),
        (
          "Site Stats",
          {
                "fields" : ["last_login", "date_joined"], 
          } ,
        ),
    ]

admin.site.register(DashboardUser, UserAdmin)



"""
# Register your models here.
from .models import ToDoItem

class ToDoItemAdmin(admin.ModelAdmin):
    readonly_fields = ['id',]
    raw_id_fields=['task_author',]

admin.site.register(ToDoItem,ToDoItemAdmin)
"""
