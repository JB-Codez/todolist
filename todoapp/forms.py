from django import forms
from django.forms import ModelForm, Textarea, TextInput, CheckboxInput

from .models import ToDoItem

INPUT_CLASSES = 'w-full py-4 px-6 border mt-4 mb-6'
EDIT_CLASS = 'w-full py-4 mt-6 mb-8 auto pt-6 pb-16 pl-3 pr-3 rounded bg-stone-50'
EDIT_BOX = 'rounded w-8 align-middle m-3'

class TaskForm(ModelForm):
    class Meta:
        model = ToDoItem # The model we're working on 
        fields = ('task_description',)


        widgets = {
            'task_description': forms.Select(attrs={
                #'class': INPUT_CLASSES,
                
            }),
            'task_description': TextInput(attrs={'placeholder':'Add new task ...',
                                                 'class':INPUT_CLASSES, })
            
        }



class EditForm(ModelForm):
    class Meta:
        model = ToDoItem
        fields = ('task_description', 'task_complete',)
        
        widgets = {
            'task_description': TextInput(attrs={'class':EDIT_CLASS}),
            'task_complete': CheckboxInput(attrs={'class': EDIT_BOX}),
            
        }
        



