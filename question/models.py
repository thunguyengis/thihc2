from django.db import models

# Create your models here.
from datetime import datetime 
#from django.utils.timezone
from django.utils import timezone
from django.contrib.auth.models import User
from configurations.models import CoursOfDepartment
from exam.models import Exam
# gia trj nhỏ nhất giá trị lớn nhất
from django.core.validators import MaxValueValidator, MinValueValidator
# các dữ liệu khác
from ckeditor.fields import RichTextField
#from ckeditor_uploader.fields import RichTextUploadingField

class Question_Type(models.Model):
    question_type_name = models.CharField(max_length=200, null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
class Question(models.Model):
    coursOfDepartment = models.ForeignKey(CoursOfDepartment, on_delete=models.CASCADE)
    chapter = models.IntegerField(default=0)
    #question_type = models.ForeignKey(Question_Type, on_delete=models.CASCADE)
    question_level = models.CharField(max_length=200, null=True)
    question_type = models.CharField(max_length=200, null=True)
    question_name = models.TextField(default="-", null=True)
    question_content = RichTextField(blank=True,null=True)

    correct_answer = models.TextField(default="-", null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_name = models.TextField( null=True)
    choice_content = RichTextField(blank=True,null=True)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)

class QuestionOfExam(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

class Answer(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_name = models.TextField( null=True)
    answer_list = models.TextField( null=True)
    answer_name = models.TextField( null=True)
    user_answer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default = timezone.now, editable=False)
    updated_at  = models.DateTimeField(default = timezone.now, editable=False)
    order = models.IntegerField(default=0)
