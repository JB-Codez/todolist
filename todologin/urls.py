from django.urls import path

from . import views
# refactor/src:  https://youtu.be/CA5duCGDSUE
# src: https://docs.djangoproject.com/en/4.2/howto/static-files/
from django.conf import settings
from django.conf.urls.static import static

app_name = 'todologin'

urlpatterns = [
    
    #path('login', views.login_view, name="login_in_django"),
    # path('signup/', views.signup_view, name="signup_in_django"),
    path('', views.sign_up, name='signup_in_django'),
    #path('logout/', views.logout_view, name="logout_in_django"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this is a helper function
# and only works in debug mode and should be discarded during production
# src: https://docs.djangoproject.com/en/4.2/howto/static-files/
# 3 implementation of this and the above x2 Import statements


"""

http://127.0.0.1:8000/login/                =       path('login/', views.login_view, name="login_in_django"),
                                            =       path('login', views.login_view, name="login_in_django"),
"""