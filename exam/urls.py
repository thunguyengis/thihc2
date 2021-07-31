from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static
app_name = 'exam'

urlpatterns = [
   path('', views.index, name = 'index'),
   path('create/', views.create, name = 'create'),
   path('active/', views.active, name = 'active'),
   path('room/', views.room, name = 'room'),
   path('add_room/', views.add_room, name = 'add_room'),
   path('detail_room/<int:exam_id>', views.detail_room, name = 'detail_room'),
   path('detail_question/<int:exam_id>', views.detail_question, name = 'detail_question'),
   path('setting_question/<int:exam_id>', views.setting_question, name = 'setting_question'),
   path('ajax/load_sections/', views.load_sections, name='ajax_load_sections'),  # <-- this one here
   path('ajax/load_courses/', views.load_courses, name='ajax_load_courses'),  # <-- this one here
   path('thu/', views.thu, name='thu'),  # <-- this one here

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

