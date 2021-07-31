from django import forms
from django.forms import   ModelForm
from .models import Exam, GradeOfExam, Room
from configurations.models import CourseOfSection, Class, Section
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy  
# Create your models here.
from datetime import datetime 
import random
import string

class ExamForm1(ModelForm):  
    
     class Meta:
        model = Exam
        fields = '__all__'
        #fields = [ 'exam_name', 'active', 'notice_published', 'birthday', 'picpath']
        widgets = {
            'year_begins': NumberInput(attrs={'type': 'datetime'}),
            'year_end': NumberInput(attrs={'type': 'datetime'})
        }
        
    

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
string.ascii_letters = '123456789abcdefghijklmnopqrstuvwxyz'
def random_char(y):
        check = True
        while check :
            code = ''.join(random.choice(string.ascii_letters) for x in range(y))
            if( Exam.objects.filter( exam_code = code).count() != 1 ):
                check = False

        return code

class ExamForm(forms.Form):
    myClass = forms.ModelChoiceField(
            queryset = Class.objects.all(),
            widget=forms.Select( attrs={'class': 'form-control'}),
           
    ) 
    section = forms.ModelChoiceField(
            queryset = Section.objects.none(),
            widget=forms.Select( attrs={'class': 'form-control'}),
           
    ) 
    courseOfSection = forms.ModelChoiceField(
            queryset = CourseOfSection.objects.none(),
            widget=forms.Select( attrs={'class': 'form-control'}),
           
    ) 

    exam_type2 = forms.MultipleChoiceField(
            required=False,
            widget=forms.Select( attrs={'class': 'form-control'}),
            choices=FAVORITE_COLORS_CHOICES,
           
        )
    exam_code = forms.CharField(
                        widget=forms.TextInput(attrs={
                                'class': 'form-control',
                                'readonly': 'true',
                                'value': random_char(5)
                            })
        )
    active = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxInput,      
        )
    notice_published = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxInput,    
        )
    result_published = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxInput,    
        )
    time_exam = forms.IntegerField(
                       
                        widget=forms.NumberInput(attrs={
                                'class': 'form-control',
                                'value':90,
                                'step':5
                            
                            })
    )

    start_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input datepicker',
           
        })
    )

    end_date = forms.DateTimeField(
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(attrs={
            'class': 'form-control datetimepicker-input datepicker',
           
        })
    )
  
class GradeOfExamForm(ModelForm):  
  
    class Meta:
        model = GradeOfExam
        fields = '__all__'
        #fields = [ 'exam_name', 'active', 'notice_published', 'birthday', 'picpath']


class RoomForm(forms.Form):
    room_name = forms.CharField(
                    required=True, label= gettext_lazy('Room Name'),
                    widget=forms.DateTimeInput(attrs={
                            'class': 'form-control',
                        
                    })
        )
    room_number_test = forms.IntegerField(
                        label= gettext_lazy('Number Test'),
                        widget=forms.DateTimeInput(attrs={
                                'class': 'form-control',
                            
                            })
    )
  


