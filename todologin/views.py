from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
# https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-out
from django.contrib.auth import authenticate, login, logout

from .forms import UserCreationForm, UserSignInForm, RegistrationForm

from django.contrib.auth import login, logout, authenticate # https://youtu.be/WuyKxdLcw3w

from django.contrib.auth.models import User
# https://stackoverflow.com/a/17874111
from django.contrib.auth import get_user_model

# Src: https://docs.djangoproject.com/en/4.2/topics/auth/default/#how-to-log-a-user-out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

def login_view(request):
    
 
    login_form = UserSignInForm(request.POST or None)
    if request.POST and login_form.is_valid():
        user = login_form.login(request)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        
    return render(request, 'todologin/registration/login.html', {'form': login_form, 'num_visits': num_visits})




# refactored from: https://youtu.be/WuyKxdLcw3w
def sign_up(request):

    
    login_form = RegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return HttpResponseRedirect('/home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/sign_up.html', {'form': form} ) # << potential error






