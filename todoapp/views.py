from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import authenticate
from django.contrib import messages

from django.contrib.auth.decorators import login_required

import datetime

from django.db.models import Q
from todologin.models import DashboardUser
from .models import ToDoItem

from .forms import TaskForm, EditForm

from django.apps import apps

PREVIEW_TEXT = "PRIVATE TASK"

# Return either admin + public tasks OR admin + user specific/logged in tasks
def user_todolist(request):
    # we pass the user
    # we filter 
    # we want to separate what is passed from the view, i.e. don't filter inside the 
    # view because, then you're sending the entire data set .. SO
    # filter before hand, HOWEVER, i also want to SEE the presence of a filtered
    # to do (i.e. hinting at tasks that others have. ) so each non user task should
    # default to a dummy secret task. 
    # so, we cycle through each element, and if it is NOT the user
    # we replace it with a dummy task - i.e. 'Premium sneak preview'

    try:
        if ToDoItem.objects.all():
            pass
    except:
        return HttpResponseRedirect('/')
    all_tasks = ToDoItem.objects.all()

    returned_list = []

    if request.user.is_authenticated:
        tasks_all = ToDoItem.objects.all()
        user_admin = DashboardUser.objects.get(username="admin")
        tasks_admin_and_user = []
        # capture admin + logged in user tasks (i.e. private tasks)
        for task in tasks_all:
            if (task.task_author == request.user): # or (task.task_author == user_admin):
                tasks_admin_and_user.append(task)
            elif(task.task_author == user_admin):
                # user task
                if(task.task_is_private != True):
                    # public task - everyone sees
                    tasks_admin_and_user.append(task)
                else:
                    # private task - only admin sees
                    user_admin_dummy = DashboardUser.objects.get(username="admin")
                    
                    private_task = task
                    private_task.task_description=PREVIEW_TEXT
                    private_task.task_complete= False
                    private_task.task_is_private=True
                    
                    tasks_admin_and_user.append(private_task)
            elif (task.task_is_private != True):
                tasks_admin_and_user.append(task) 
            else:
                user_admin_dummy = DashboardUser.objects.get(username="admin")
                
                private_task = task
                private_task.task_description=PREVIEW_TEXT
                private_task.task_complete= False
                private_task.task_is_private=True
                
                tasks_admin_and_user.append(private_task)
        returned_list = tasks_admin_and_user      
    else:
        # capture admin + public tasks
        tasks_all = ToDoItem.objects.all()
        tasks_for_non_accounts = []
        for task in tasks_all:
            if task.task_is_private:
                user_admin_dummy = DashboardUser.objects.get(username="admin")
                # dummy storage
                private_task = task
                private_task.task_description=PREVIEW_TEXT
                private_task.task_complete= False
                private_task.task_is_private=True
                tasks_for_non_accounts.append(private_task)
            else:
                tasks_for_non_accounts.append(task)
        returned_list = tasks_for_non_accounts    
    context = {
        "returned_list" : returned_list,
    }
    return context

def index_todoapp(request):
    # Main page
    # Display a list of tasks, some hidden (if the task is hidden)
    # and the current user is not the task owner, allow anyone
    # to add/edit/delete shared tasks, make unique/their own
    # tasks and edit/delete/add private tasks
    if request.method == "POST":
        if 'submit' in request.POST:
            # Create a form instance and populate it with data from the request:
            form_view = TaskForm(request.POST) # https://docs.djangoproject.com/en/4.2/topics/forms/#:~:text=if%20request.method%20%3D%3D%20%22POST%22%3A
            # Is this form filled with valid information? 
            if form_view.is_valid():    
                if request.user.is_authenticated:
                    # SOMEONE IS LOGGED IN
                    task = form_view.save(commit=False)
                    task_author = request.user
                    task.task_author = task_author
                    task.save()

                    tasks_all = ToDoItem.objects.all()
                    user_admin = DashboardUser.objects.get(username="admin")
    
                    tasks_admin_and_user = []
                    
                    for task in tasks_all:
                        """ DEBUG:
                        if (task.task_author == user_admin) :
                            print("user_admin entry found at for task " + task.task_description )
                        if (task.task_author == request.user) :
                            print(" a task for this user: " + request.user.username + ", has been found: " + task.task_description)
                        """
                        if(task.task_author == user_admin) or (task.task_author == request.user):
                            tasks_admin_and_user.append(task)
                    form_view = TaskForm()
                    return HttpResponseRedirect('/')
                else:
                    if DashboardUser.objects.filter(username='admin').exists():
                        task = form_view.save(commit=False)
                        adminUser = DashboardUser.objects.get(username='admin')
                        if adminUser:
                            task.task_author = adminUser
                            task.save()
                            form_view = TaskForm()
                            return HttpResponseRedirect('/')
                    else:
                                      
                        #IMPORTANT TO NOTE: IF ADMIN IS ALREADY A USER THIS DOESNT CREATE ONE
                        # Create a new admin
                        admin_new = DashboardUser.objects.create_user(username='admin', email='admin@admin.com',password='simplepass123')
                     
                        task = form_view.save(commit=False)
                        adminUser = DashboardUser.objects.get(username='admin')
                        task.task_author = adminUser
                        task.save()
                        form_view = TaskForm()
                        return HttpResponseRedirect('/')
        else:
            form_view = TaskForm
    else:
        # A redirect comes here because the method is a GET; i.e. the first time or non-form POST request
        form_view = TaskForm 

    todolist = ToDoItem.objects.order_by('id')

    context = user_todolist(request) 
    todolist = context['returned_list']
    
    current_user = request.user
    
    """
    # logic for the background profile pics
                        <!-- see if the task is private -->
                        <!-- get the user who created the task -->
                        
                        <!-- see if the user has a profile pic -->

                        <!-- if the user has a profile pic, set it to background -->
                        <!-- if no user profile pic, set to defult background -->
       choosing to do logic here and not in html because this is the CONTROLLER
       the trick is, the tasks, do not store user info, and we want to be
       able to change task owners, so we are only pointing to the user,
       not to the image, of the user, which is in the user data SO
       we need to create a parallel list for each task and copy in the
       image address for each user tied to each.
       Got this feature to work, but ultimately excised it out, due to
       need for multiple divs etc and too cluttered an UI          
    """
    #task_user_images = []
    
    task_abs_path_images=[]
    beginfix = '/media/'
    task_str_paths=[]
    
    
    for task_in in todolist:
        
        profile_pic_flag = False
        # Get the user who created the task
        task_author_ = task_in.task_author
        
        # Test if the task user has a profile pic
        # No need we have now defaulted
        
        if task_in.task_is_private and current_user != task_author_:
            # Task Private                          = YES; 
            # Task owner IS the browser user        = NO
            # Dummy image
            # THIS is the special case where we show dummy
            # BUT instead, lets just add the admin image.
          
            # IMPORTANT TO NOTE: IF ADMIN IS ALREADY A USER THIS DOESNT CREATE ONE
            # Create a new admin
            if DashboardUser.objects.filter(username='admin').exists():
                
                admin_user = DashboardUser.objects.get(username='admin')
                admin_profile_pic = admin_user.user_image
               
            else:
                admin_new = DashboardUser.objects.create_user(username='admin', email='admin@admin.com',password='simplepass123',user_image='profile_pics/no_prof_pic.PNG')
                admin_user = DashboardUser.objects.get(username='admin')
                admin_profile_pic = admin_user.user_image
            

            #task_user_images.append({'image': admin_profile_pic, 'idkey': task_in.pk })
            temp = beginfix + str(admin_profile_pic) 
            task_abs_path_images.append({'image': temp, 'idkey': task_in.pk   })
        elif task_in.task_is_private and current_user == task_author_:
            # Task Private                          = YES; 
            # Task owner IS the browser user        = YES
            #task_user_images.append({'image': task_author_.user_image, 'idkey': task_in.pk})
            temp = beginfix + str(task_author_.user_image) 
            task_abs_path_images.append({'image':temp, 'idkey': task_in.pk   })
        else:
            # Task Private                          = NO
            # Task owner IS the browser user        = YES/NO
            temp = '/media/profile_pics/' 

            #task_user_images.append({'image': task_author_.user_image, 'idkey': task_in.pk})
            temp = beginfix + str(task_author_.user_image) 
            task_abs_path_images.append({'image':temp , 'idkey': task_in.pk   })

        """
        # For future Debugs
        #for tasko in task_user_images:
        #   print(tasko['image'])
        #   print(tasko['idkey'])
        # See if the user has a profile pic
        print(type(task_author_))
        if task_author_.user_image:
            profile_pic_flag = True
            print('they have a user image!!!!!!!!!!!!!!!!!!')
            task_user_images.append({'image': task_author_.user_image, 'idkey': task_in.pk})
            print(task_in.pk)
        else:
            print('this mfer dont have a  PHOTOG   ??????')
            task_user_images.append({'image': "profile_pics/no_prof_pic.PNG", 'idkey': task_in.pk })
        
        """           

        
    return render(request, 'todoapp/todo_index.html',
                  {
                    'form': form_view, 
                    'to_do_list' : todolist,  
                    #'task_user_images':task_user_images, #no longer used
                    'current_user': current_user,#no longer used
                    'task_abs_path_images':task_abs_path_images,#no longer used
                   }
   )
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
    

def editTask(request, task_id):
    # refactor 8.18.23
    # src: https://stackoverflow.com/a/3243509
    try:
        taskToEditOne = ToDoItem.objects.get(pk=task_id)
    except ToDoItem.DoesNotExist:
        # Failsafe redirect
        return HttpResponseRedirect('/')

    taskToEdit = ToDoItem.objects.get(pk=task_id)
    
    # Private task check
    if(taskToEdit.task_is_private):
        current_user = request.user
        if current_user != taskToEdit.task_author:
            #SRC: https://docs.djangoproject.com/en/4.2/ref/contrib/messages/#using-messages-in-views-and-templates
            # messages.add_message(request, messages.INFO, "Please login to continue") # displaying in reg/login.html - too cluttered
            # Wrong user logged in/can't access that 
            return HttpResponseRedirect('/login/')
    taskForm = EditForm(instance=taskToEdit)

    if request.method == 'POST':
        taskForm = EditForm(request.POST, instance=taskToEdit)
        if taskForm.is_valid():
            taskForm.save()
            return HttpResponseRedirect('/')    
    return render(request, 'todoapp/edit.html',
                  {'task': taskToEdit,
                   'form': taskForm,}
  )

def deleteTask(request, task_id):
    
    # refactor 8.18.23 - matching the editTask
    # src: https://stackoverflow.com/a/3243509
    try:
        taskToDeleteOne = ToDoItem.objects.get(pk=task_id)
    except ToDoItem.DoesNotExist:
        return HttpResponseRedirect('/')
    
    taskToDelete = ToDoItem.objects.get(pk=task_id)
    
    # Private task check
    if(taskToDelete.task_is_private):
        current_user = request.user
        if current_user != taskToDelete.task_author:
            return HttpResponseRedirect('/login/')
    taskForm = EditForm(instance=taskToDelete)
    
    # Only pass the text not the editable item - that way this is ONLY delete section
    taskDescription = taskToDelete.task_description
        
    if request.method == 'POST':
        if 'submit-deletion' in request.POST:
            taskToDelete.delete()
        return HttpResponseRedirect('/')    

    return render(request, 'todoapp/delete.html',
                  {'task': taskToDelete,
                   'taskDescription': taskDescription,
                   'form': taskForm,}
   )

