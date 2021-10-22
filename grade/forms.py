from django import forms
from django.forms import   ModelForm
from exam.models import Exam, GradeOfExam, Room
from configurations.models import CourseOfSection, Class, Section

from django.utils.translation import gettext_lazy  
# Create your models here.


#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#

FAVORITE_COLORS_CHOICES = [
    ('coefficient_1_1', 'Hệ Số 1 Lần 1'),
    ('coefficient_1_2', 'Hệ Số 1 Lần 2'),
    ('coefficient_2_1', 'Hệ Số 2 Lần 1'),
    ('coefficient_2_2', 'Hệ Số 2 Lần 2 '),
    ('end_mark_1_1', 'Thi kết thúc môm '),
    ('coefficient_v2_1_1', 'Hệ Số 1 Lần 1 Thi lại'),
    ('coefficient_v2_1_2', 'Hệ Số 1 Lần 2 Thi lại'), 
    ('coefficient_v2_2_1', 'Hệ Số 2 Lần 1 Thi lại'),
    ('coefficient_v2_2_2', 'Hệ Số 2 Lần 2 Thi lại'),
    ('end_mark_v2_1_1', 'Thi kết thúc môm Thi lại'),
]
#=====================
#string.ascii_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'


class SummaryForm(forms.Form):
    myClass = forms.ModelChoiceField(
            queryset = Class.objects.all(),
            widget=forms.Select( attrs={'class': 'form-control'}),
            label= gettext_lazy('myClass')
           
    ) 
    section = forms.MultipleChoiceField(
            
            widget=forms.SelectMultiple( attrs={'class': 'form-control '}),
            label= gettext_lazy('section')
           
    ) 
   

   
  

