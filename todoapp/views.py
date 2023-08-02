from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render

from django.http import HttpResponseRedirect

from .models import ToDoItem
from .forms import TaskForm, EditForm

def index_todoapp(request):
    
    an_edit_is_pressed = False
    
    
    print('index has arrived')
    submitted = False # did someone come here first time? or have they already submitted info?
    print(request.method)
    # we designate that our form is posting in our html file
    if request.method == "POST":
        if 'submit' in request.POST:
            print('we have a submitt submitted')
            print('here in my post')
            # create a form instance and populate it with data from the request:
            
            
            form_view = TaskForm(request.POST) # https://docs.djangoproject.com/en/4.2/topics/forms/#:~:text=if%20request.method%20%3D%3D%20%22POST%22%3A
            #is this form filled with valid information? 
            if form_view.is_valid():
                print('everything is valid here')
                form_view.save()
                #redirect user back to self
                #return HttpResponseRedirect('/?submitted=True')
                return HttpResponseRedirect('/')
                # can probably omit submitted entirely
                # redirects 
                # return HttpResponseRedirect('/?submitted=True')
        elif 'edit' in request.POST:
            print('lets get editiable')
            form_view = TaskForm
        
        elif 'delete' in request.POST:
            print('darth delete')
            form_view = TaskForm
        else:
            form_view = TaskForm
    else:
        # a redirect comes here becaust the method is a GET
        print('everything ELSE is here')
        form_view = TaskForm # declaring our form object
        if 'submitted' in request.GET:
            submitted = True
            print('doth the TRUTH')
    print('time to return')
    todolist = ToDoItem.objects.order_by('id')
    
   
    
    return render(request, 'todoapp/todo_index.html',
                  {'form': form_view, "to_do_list" : todolist,}
                  #{'form': form_view, 'submitted':submitted, "to_do_list" : todolist,} #<--pass our form into a context dictionary through views.py
    )
    
    """
    todolist = ToDoItem.objects.order_by('id')
        
    template = loader.get_template("todoapp/todo_index.html")
    
    
    form_new_task = TaskForm()
    
    
    
    context = {
        "form_new_task" : form_new_task,
        "to_do_list" : todolist,
    }
    
    
    context = {
        "to_do_list" : todolist,
        
    }
    #output = ", \n".join([t.task_description for t in todolist])
        
    if request.method == 'POST':
        print('Hello')
        form_here = TaskForm(request.POST)
        if form_here.is_valid():
            print("looks valid")
            data = request.POST.dict()
            task_description = data.get("task_description")
            print(task_description)
            print(form_here.cleaned_data['task_description'])
            
            p=form_here.cleaned_data['task_description']
            print(p)
            
        
    
    return HttpResponse(template.render(context,request))
    """
    

def editTask(request, task_id):
    
    
    #taskToEdit = ToDoItem.objects.get(pk=task_id)
    # with failsafe
    taskToEdit = get_object_or_404(ToDoItem,pk=task_id)
    
    taskForm = EditForm(instance=taskToEdit)
    
    
    if request.method == 'POST':
        print('why yes')
        taskForm = EditForm(request.POST, instance=taskToEdit)
        if taskForm.is_valid():
            print('pretty valid too')
            taskForm.save()
            return HttpResponseRedirect('/')    
    
    return render(request, 'todoapp/edit.html',
                  {'task': taskToEdit,
                   'form': taskForm,}
                  #{'form': form_view, 'submitted':submitted, "to_do_list" : todolist,} #<--pass our form into a context dictionary through views.py
    )
    
def deleteTask(request, task_id):
    taskToDelete = get_object_or_404(ToDoItem,pk=task_id)
    taskForm = EditForm(instance=taskToDelete)
    
    taskDescription = taskToDelete.task_description
        
    if request.method == 'POST':
        print('deleting the submitted') 
        #ToDoItem.objects.filter(id=taskToDelete).delete()
        if 'submit-deletion' in request.POST:
            taskToDelete.delete()
            print('uh oh?? deleted')
        else:
            print('testing to delete here')
        print('back home baybeee!')
        return HttpResponseRedirect('/')    

            
    
    return render(request, 'todoapp/delete.html',
                  {'task': taskToDelete,
                   'taskDescription': taskDescription,
                   'form': taskForm,}
                  #{'form': form_view, 'submitted':submitted, "to_do_list" : todolist,} #<--pass our form into a context dictionary through views.py
    )