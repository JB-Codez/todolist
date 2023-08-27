from django import forms
from django.forms import ModelForm, Textarea, TextInput, CheckboxInput

from .models import ToDoItem

INPUT_CLASSES   = 'w-full border mt-4 mb-6 px-2 py-4'
EDIT_CLASS      = 'auto w-full bg-stone-50 mt-6 mb-8 py-4 pt-6 pr-3 pb-16 pl-3 rounded'
EDIT_BOX        = 'w-8 align-middle m-3 rounded'

class TaskForm(ModelForm):
    class Meta:
        model = ToDoItem # The model we're working on 
        fields = ('task_description',)


        widgets = {
            'task_description': TextInput(attrs={'placeholder':'Add a new task ...',
                                                 'class':INPUT_CLASSES, })  
        }



class EditForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ('task_description', 'task_complete', 'task_is_private')
        
        widgets = {
            'task_description': TextInput(attrs={'class':EDIT_CLASS}),
            'task_complete': CheckboxInput(attrs={}),
            'task_is_private': CheckboxInput(attrs={}),
            
        }
        



