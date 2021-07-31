from django.db import models

# Create your models here.
from datetime import datetime 
#from django.utils.timezone
from django.utils import timezone
from django.contrib.auth.models import User
from configurations.models import Student,  CourseOfSection
# gia trj nhỏ nhất giá trị lớn nhất
from django.core.validators import MaxValueValidator, MinValueValidator


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(CourseOfSection, on_delete=models.CASCADE)
    present = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
  
    order = models.IntegerField(default=0)
    