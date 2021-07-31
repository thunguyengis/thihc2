from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

app_name = 'course'

urlpatterns = [
   path('', views.index, name='course'),
   path('<int:section_id>/section/', views.section, name='section'),
   path('teacher/', views.teacher, name='teacher'),

   #path('<int:question_id>/vote/', views.vote, name='vote'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

