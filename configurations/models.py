from django.db import models

# Create your models here.
from datetime import datetime 
#from django.utils.timezone
from django.utils import timezone
from django.contrib.auth.models import User

# năm bắt đầu vào học và kết thúc của lớp
from django.core.validators import MaxValueValidator, MinValueValidator

# đe tạo form trong model
from django import forms
from django.forms import  CharField, DateField, ModelForm, DateInput, Textarea
from django.forms.widgets import NumberInput


class Configurations(models.Model):
    name = models.CharField(max_length=200, null=True)
    established = models.CharField(max_length=200, null=True)
    about = models.TextField(default="-", null=True)
    medium =models.CharField(max_length=200, null=True)
    code = models.IntegerField(null=True, unique=True)
    theme = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.name


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picpath =  models.ImageField(upload_to ='uploads/% Y/% m/% d/', null=True)
    gender = models.CharField(max_length=100, null=True)
    def get_picpath(self):
        return self.picpath

'''
   tao bảng departments phòng khoa ban thuộc nhà trường
'''
class Department(models.Model):
    department_name = models.CharField(verbose_name="Cơ quan", max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.department_name

class CoursOfDepartment(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    course_name = models.CharField(verbose_name="Môn Giảng Dạy", max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.course_name

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    #student_name = models.CharField(max_length=200, null=True)
    birthday = models.DateField()
    #religion = models.CharField(max_length=200, null=True)
    picpath =  models.ImageField(upload_to ='uploads', null=True)
    #gender = models.CharField(max_length=100, null=True)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    def getname(self):
        return self.user.last_name + " " + self.user.first_name 

'''
   Loại hình đào tạo, hệ số tính điểm môn học

class TypeOfEducation(models.Model):
    TypeOfEducation_name = models.CharField(max_length=200, null=True)
    coefficient1 = models.IntegerField(default=0)
    coefficient2 = models.IntegerField(default=0)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.majors_name
'''

'''
   tao bảng ngành học, lớp học
'''
class Majors(models.Model):
    majors_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.majors_name

# xác định thời gian 
def current_year():
    return datetime.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year()+5)(value) 
def min_value_current_year(value):
    return MinValueValidator(current_year())(value) 

class Class(models.Model):
    class_name = models.CharField(max_length=200, null=True)
    majors = models.ForeignKey(Majors, on_delete=models.CASCADE)
    year_begins = models.IntegerField(default = current_year(), validators=[min_value_current_year, max_value_current_year])
    year_end = models.IntegerField(default = current_year(), validators=[min_value_current_year, max_value_current_year])
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.class_name

class ClassForm(ModelForm):
    class Meta:
        model = Class
        fields = '__all__'
        """widgets = {
            'year_begins': NumberInput(attrs={'type': 'date'}),
            'year_end': NumberInput(attrs={'type': 'date'})
        }
        """
   

# học phần, học kỳ
class Section(models.Model):
    section_name = models.CharField(max_length=200, null=True)
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.section_name

# course môn học
class Course(models.Model):
    course_name = models.CharField(max_length=200, null=True)
    course_time = models.CharField(max_length=200, null=True)
    grade_system_name = models.CharField(max_length=200, null=True)
    quiz_count = models.IntegerField(default=0)
    assignment_count = models.IntegerField(default=0)
    ct_count = models.IntegerField(default=0)
    quiz_percent = models.IntegerField(default=0)

    attendance_percent = models.IntegerField(default=0)
    assignment_percent = models.IntegerField(default=0)
    ct_percent = models.IntegerField(default=0)
    final_exam_percent = models.IntegerField(default=0)

    practical_percent = models.IntegerField(default=0)
    att_fullmark = models.IntegerField(default=0)
    quiz_fullmark = models.IntegerField(default=0)
    a_fullmark = models.IntegerField(default=0)

    ct_fullmark = models.IntegerField(default=0)
    final_fullmark = models.IntegerField(default=0)
    practical_fullmark = models.IntegerField(default=0)
    a_fullmark = models.IntegerField(default=0)

   
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    section = models.ForeignKey(Section, on_delete=models.CASCADE) 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    start_date = models.DateTimeField(default = timezone.now)
    end_date  = models.DateTimeField(default = timezone.now)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.course_name
# course môn học
class CourseOfSection(models.Model):
    course_name = models.CharField(max_length=200, null=True)
    course_time = models.CharField(max_length=200, null=True)
    grade_system_name = models.CharField(max_length=200, null=True)
    quiz_count = models.IntegerField(default=0)
    assignment_count = models.IntegerField(default=0)
    ct_count = models.IntegerField(default=0)
    quiz_percent = models.IntegerField(default=0)

    attendance_percent = models.IntegerField(default=0)
    assignment_percent = models.IntegerField(default=0)
    ct_percent = models.IntegerField(default=0)
    final_exam_percent = models.IntegerField(default=0)

    practical_percent = models.IntegerField(default=0)
    att_fullmark = models.IntegerField(default=0)
    quiz_fullmark = models.IntegerField(default=0)
    a_fullmark = models.IntegerField(default=0)

    ct_fullmark = models.IntegerField(default=0)
    final_fullmark = models.IntegerField(default=0)
    practical_fullmark = models.IntegerField(default=0)
    a_fullmark = models.IntegerField(default=0)

   
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE) 
    section = models.ForeignKey(Section, on_delete=models.CASCADE) 
    coursOfDepartment = models.ForeignKey(CoursOfDepartment, on_delete=models.CASCADE) 
    
    user = models.ForeignKey(User, on_delete=models.CASCADE) 

    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    start_date = models.DateTimeField(default = timezone.now)
    end_date  = models.DateTimeField(default = timezone.now)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.coursOfDepartment.course_name
    def getclass(self):
        return self.section.myclass.class_name
    def getname(self):
        return self.user.last_name + " " + self.user.first_name

# học viên
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    myclass = models.ForeignKey(Class, on_delete=models.CASCADE)
    #student_name = models.CharField(max_length=200, null=True)
    birthday = models.DateField()
    religion = models.CharField(max_length=200, null=True)
    picpath =  models.ImageField(upload_to ='uploads', null=True)
    gender = models.CharField(max_length=100, null=True)
    year_begins = models.IntegerField(default = current_year())
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.user.username
    def getname(self):
        return self.user.last_name + " " + self.user.first_name 



'''
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
'''
class Grade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    marks = models.FloatField(default=0, null=True)
    attendance = models.FloatField(default=0, null=True)
    quiz1 = models.FloatField(default=0, null=True)
    quiz2 = models.FloatField(default=0, null=True)
    quiz3 = models.FloatField(default=0, null=True)
    quiz4 = models.FloatField(default=0, null=True)
    quiz5 = models.FloatField(default=0, null=True)
    ct1 = models.FloatField(default=0, null=True)
    ct2 = models.FloatField(default=0, null=True)
    ct3 = models.FloatField(default=0, null=True)
    ct4 = models.FloatField(default=0, null=True)
    ct5 = models.FloatField(default=0, null=True)
    assignment1 = models.FloatField(default=0, null=True)
    assignment2 = models.FloatField(default=0, null=True)
    assignment3 = models.FloatField(default=0, null=True)
    written = models.FloatField(default=0, null=True)
    mcq = models.FloatField(default=0, null=True)
    practical = models.FloatField(default=0, null=True)


    #exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    #student_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    def get_picpath(self):
        return self.pic_path


class GradeOfVN(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_mark_exam = models.FloatField(default=0, null=True)
    total_mark_course = models.FloatField(default=0, null=True)
    total_marks = models.FloatField(default=0, null=True)
    coefficient_1_1 = models.FloatField(default=0, null=True)
    coefficient_1_2 = models.FloatField(default=0, null=True)
    coefficient_v2_1_1 = models.FloatField(default=0, null=True)
    coefficient_v2_1_2 = models.FloatField(default=0, null=True)
    coefficient_2_1 = models.FloatField(default=0, null=True)
    coefficient_2_2 = models.FloatField(default=0, null=True)
    coefficient_v2_2_1 = models.FloatField(default=0, null=True)
    coefficient_v2_2_2 = models.FloatField(default=0, null=True)
    practical_1_1 = models.FloatField(verbose_name="Thực hành",default=0, null=True)
    practical_v2_1_1 = models.FloatField(verbose_name="Thực hành",default=0, null=True)
    end_mark_1_1 = models.FloatField(default=0, null=True)
    end_mark_v2_1_1 = models.FloatField(default=0, null=True)
    #exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    courseOfSection = models.ForeignKey(CourseOfSection, on_delete=models.CASCADE)
    #student_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    def get_picpath(self):
        return self.pic_path


 

    