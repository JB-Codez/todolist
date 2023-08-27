from django.contrib import admin
from django.urls import path, include

#from todoapp.views import index_todoapp


# refactor/src:  https://youtu.be/CA5duCGDSUE
# src: https://docs.djangoproject.com/en/4.2/howto/static-files/
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', include("todoapp.urls")),
    path('admin/', admin.site.urls), # works with admin too  , i.e. no
    #path('home/',index_todoapp, name='homepage'),
    #path('/',include("todologin.urls")),
    #path('accounts/', include("todologin.urls")),
    path('',include('django.contrib.auth.urls')), #https://docs.djangoproject.com/en/4.2/topics/auth/default/#using-the-views
    # accounts/login/ [name='login']
    # accounts/logout/ [name='logout']
    # accounts/password_change/ [name='password_change']
    # accounts/password_change/done/ [name='password_change_done']
    # accounts/password_reset/ [name='password_reset']
    # accounts/password_reset/done/ [name='password_reset_done']
    # accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
    # accounts/reset/done/ [name='password_reset_complete']
    #                             
    path('sign-up',include("todologin.urls")),
    #path('signup/',include("todoapp.urls")),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this is a helper function
# and only works in debug mode and should be discarded during production
# src: https://docs.djangoproject.com/en/4.2/howto/static-files/
#  2 implementation of this and the above x2 Import statements
""" 
src: https://docs.djangoproject.com/en/4.2/topics/auth/default/#using-the-views
included with:path('',include('django.contrib.auth.urls'))

>>>
accounts/login/ [name='login']
accounts/logout/ [name='logout']
accounts/password_change/ [name='password_change']
accounts/password_change/done/ [name='password_change_done']
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']


"""