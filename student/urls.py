from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

app_name = 'student'

urlpatterns = [
   #path('', views.index, name='student'),
   path('<int:section_id>/section/', views.sectionStudent, name='section'),
   path('<int:class_id>/class/', views.classStudent, name='class'),

   path('import/', views.importStudent, name='importStudent'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

