from django import forms
from django.forms import   ModelForm, TextInput, Select,  CharField
from .models import Student, User, Class, Teacher, Section, Course, CourseOfSection
from django.forms.widgets import NumberInput
from django.utils.translation import gettext_lazy  

class StudentForm1(forms.Form):
     #user = models.OneToOneField(User, on_delete=models.CASCADE)
     #myclass = models.ForeignKey(Class, on_delete=models.CASCADE)
     myclass = forms.ModelChoiceField(queryset=Class.objects.all(), widget=forms.TextInput( attrs={'class': 'form-control'}),)
     student_name = forms.CharField(max_length=200, widget=forms.TextInput( attrs={'class': 'form-control'}) )
     birthday = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
     religion = forms.CharField(max_length=200,  widget=forms.TextInput( attrs={'class': 'form-control'}))
     #picpath =  forms.ImageField()
     gender = forms.CharField(max_length=100, widget=forms.TextInput( attrs={'class': 'form-control'}))
     order = forms.IntegerField(widget=forms.NumberInput( attrs={'class': 'form-control'}))
     
class StudentForm(ModelForm):
    first_name = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}), label= gettext_lazy('First Name'))
    last_name = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}), label= gettext_lazy('Last Name'))
    code_student = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}), label= gettext_lazy('code_student'))
    #birthday = forms.DateField(input_type='date' ,template_name = 'django/forms/widgets/date.html')
    class Meta:
        model = Student
        fields = [ 'first_name', 'last_name', 'code_student', 'myclass','birthday', 'religion', 'picpath', 'gender']
        widgets = {
            'birthday': NumberInput(attrs={'type': 'date'}),
            'myclass': Select( attrs={'class': 'form-control'}),
            'religion': TextInput(attrs={  'class': 'form-control',}),   
            'gender': TextInput(attrs={  'class': 'form-control',}),   
        }
class TeacherForm(ModelForm):
    #first_name = forms.CharField(label ="Tên")
    first_name = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}), required=True, label= gettext_lazy('First Name'))
    last_name = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}),required=True, label= gettext_lazy('Last Name'))
    code_teacher = forms.CharField(widget=forms.TextInput( attrs={'class': 'form-control'}), required=True, label= gettext_lazy('Code Teacher'))
    #birthday = forms.DateField(input_type='date' ,template_name = 'django/forms/widgets/date.html')
    class Meta:
        model = Teacher
        fields = [ 'first_name', 'last_name', 'code_teacher', 'department','birthday', 'picpath']
        widgets = {
            'department': Select( attrs={'class': 'form-control'}),
            'birthday': NumberInput(attrs={'type': 'date','class': 'form-control'})
        }  
class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = '__all__'

class CourseForm(ModelForm):
    
    class Meta:
        model = Course
        fields = [ 'course_name', 'teacher', 'course_time']
        widgets = {
            'course_name': TextInput(attrs={
                            'class': 'form-control',
                        
                    })
        } 

class CourseOfSectionForm(ModelForm):
    
    class Meta:
        model = CourseOfSection
        fields = [ 'coursOfDepartment', 'teacher', 'course_time']
        widgets = {
            'coursOfDepartment': Select( attrs={'class': 'form-control'}),
            'teacher': Select( attrs={'class': 'form-control'}),
            'course_time': TextInput(attrs={  'class': 'form-control',}),   
        } 
class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        widgets = {
            'class_name': TextInput( attrs={'class': 'form-control'}),
            'majors': Select( attrs={'class': 'form-control'}),
            'year_begins': NumberInput(attrs={'class': 'form-control'}),
            'year_end': NumberInput(attrs={'class': 'form-control'}),
            'order': TextInput( attrs={'class': 'form-control'}),
        }

        
    
        

    
