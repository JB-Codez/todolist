from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from django.forms import Textarea, TextInput, CheckboxInput, PasswordInput, EmailInput
from django.contrib.auth import authenticate #  https://docs.djangoproject.com/en/4.2/topics/auth/default/ + 
#  https://stackoverflow.com/a/15084809
from .models import DashboardUser

USERNAME_STYLE  = 'w-full border px-6 py-4 mt-4 mb-6'
EMAIL_STYLE     = 'w-full border px-6 py-10 mt-4 mb-6'
PASSWORD_STYLE  = 'w-full border px-6 py-4 mt-4 mb-6'

# -----------------------------
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegistrationForm(UserCreationForm):
    
    email = forms.EmailField(label="E-mail: ", required=True)
    
    
    password1 = forms.CharField(label="Password: ", widget=forms.PasswordInput(attrs={'class':'w-full py-4 px-6 border mt-4 mb-6'}))
    password2 = forms.CharField(
        label="Password confirmation: ", widget=forms.PasswordInput(attrs={'class':'w-full py-4 px-6 border mt-4 mb-6'})
    )
    
    class Meta:
        model = DashboardUser # User
        fields = ["username", "email", "password1", "password2"] # or fields = ["username","email","first_name","password1","password2"]

        widgets = {
                'username': TextInput(attrs={'label':"Username: ",
                                             'class':USERNAME_STYLE,
                                            'placeholder': 'Please enter a username'}
                                            ), 
                'password': PasswordInput(attrs={'class':PASSWORD_STYLE}),
            }   
    
        
        def clean_password2(self):
            # Check that the two password entries match
            password1 = self.cleaned_data.get("password1")
            password2 = self.cleaned_data.get("password2")
            if password1 and password2 and password1 != password2:
                raise ValidationError("Passwords don't match")
            return password2

        def save(self, commit=True):
            # Save the provided password in hashed format
            user = super().save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user  






class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class':'w-full py-4 px-6 border mt-4 mb-6'}))
    password2 = forms.CharField(
        label="Password confirmation", widget=forms.PasswordInput(attrs={'class':'w-full py-4 px-6 border mt-4 mb-6'})
    )
    class Meta:
        model = DashboardUser
        fields = ("username", "email")
        
        
        widgets = {
            'username': TextInput(attrs={'class':USERNAME_STYLE,
                                         'placeholder': 'Please enter a username'}
                                         ), 
            'password': PasswordInput(attrs={'class':PASSWORD_STYLE}),
            'email' : EmailInput(attrs={'class': EMAIL_STYLE}),
            #'password1': PasswordInput(attr={'class': PASSWORD_STYLE}),
            #'task_complete': CheckboxInput(attrs={'class': EDIT_BOX}),
            
        }   
    
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user    
    

class UserSignInForm(forms.ModelForm):
    
    
    
    class Meta:
        model = DashboardUser
        fields = ("username","password")
    username = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput)  
    
    
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user
    
    
     
        
class UserChangeForm(forms.ModelForm):
    
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = DashboardUser
        fields = ("username", "email", "user_image", )