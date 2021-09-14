from django.db import models

from django.contrib.auth.models import User
from configurations.models import Student
from exam.models import Exam
from question.models import Question

# Create your models here.
class QuestionOfStudent(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.TextField( null=True)
    choice_index = models.TextField( null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
class ChoiceOfStudent(models.Model):
    questionOfStudent = models.ForeignKey(QuestionOfStudent, on_delete=models.CASCADE)
    choice = models.TextField( null=True)
    order = models.IntegerField(default=0)