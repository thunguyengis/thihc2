from django.db import models

# Create your models here.
from datetime import datetime 
#from django.utils.timezone
from django.utils import timezone
from django.contrib.auth.models import User
from configurations.models import Class, CourseOfSection, Student
# năm bắt đầu vào học và kết thúc của lớp
from django.core.validators import MaxValueValidator, MinValueValidator



class Exam(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    courseOfSection = models.ForeignKey(CourseOfSection, on_delete=models.CASCADE)
    #myclass = models.ForeignKey(Class, on_delete=models.CASCADE,null=True)
    term =models.CharField(max_length=200, null=True)
    exam_name = models.CharField(max_length=200, null=True)
    exam_type2 = models.CharField(max_length=50, null=True)
    exam_code = models.CharField(max_length=50, null=True)
    active = models.BooleanField(default= False)
    notice_published= models.BooleanField(default= False)
    result_published = models.BooleanField(default= False)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    time_exam = models.IntegerField(default=90)
    start_date = models.DateTimeField(default = timezone.now)
    end_date  = models.DateTimeField(default = timezone.now)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.courseOfSection.coursOfDepartment.course_name
class Room(models.Model):
    room_name = models.CharField(verbose_name="Cơ quan", max_length=200, null=True)
    room_number_test = models.IntegerField(default=0)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
    def __str__(self):
        return self.room_name
class GradeOfExam(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    #teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    mark = models.FloatField(default=0, null=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    #exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    #student_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    doing_exam = models.BooleanField(default = False)
    starting_time = models.DateTimeField(null=True, editable=False)
    time_remaining = models.CharField(max_length=50, null=True)
