from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static
app_name = 'home'

urlpatterns = [
   path('', views.index, name="index"),
   #path('contact/', views.contact, name='contact'),
   #path('register/', views.register, name="register"),
   path('login/',auth_views.LoginView.as_view(template_name="home/login.html"), name="login"),
   #path('login/',auth_views.LoginView.as_view(), name="login"),
   path('logout/',auth_views.LogoutView.as_view(),name='logout'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

