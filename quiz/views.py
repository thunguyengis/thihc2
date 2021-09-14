
from math import e
from django.db.models.enums import Choices
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from configurations.models import Configurations, Student, Teacher, Class
from question.models import QuestionOfExam, Choice
from exam.views import Exam_type
from exam.models import Exam, GradeOfExam
from .models import QuestionOfStudent, ChoiceOfStudent

from datetime import datetime, date, timedelta

# thông báo lỗi
from django.contrib import messages 
import random
#Paginator
from django.core.paginator import Paginator


def checkIndex(a_list, value):
    try:
        return a_list.index(value)
    except ValueError:
        return None
def index(request):
     #lưu dữ liệu 
    if request.method == 'POST':
        
        username = request.POST['username']
        
        user = User.objects.filter(username = username).first()
        if user == None :
            messages.error(request, "Mã Học viên hoặc Mã Bài thi không tồn tại")
        else:
            student = Student.objects.filter(user_id = user.id).first()
            
            exam_code = request.POST['exam_code']
            exam = Exam.objects.filter(exam_code = exam_code).first()
            
            if exam == None :
                messages.error(request, "Mã Học viên hoặc Mã Bài thi không tồn tại")
            else:
                #return HttpResponse(student.myclass.id)
                # kiểm tra mã hv và mã bài thi 
                if student.myclass.id == exam.getClass():
                   
                    request.session['check'] = True
                    request.session['username'] = username
                    request.session['exam_code'] = exam_code
                    gradeOfExam = GradeOfExam.objects.filter( exam_id = exam.id, student_id = student.id ).first()
                    #return HttpResponse( gradeOfExam.doing_exam)
                    if gradeOfExam.doing_exam == False:
                        
                        # doing exam
                        gradeOfExam.doing_exam = True
                        gradeOfExam.save()
                        questionOfStudent = QuestionOfStudent.objects.filter( exam_id = exam.id, student_id = student.id  ).first()
                        #return HttpResponse( questionOfStudent)
                        #kiểm tra đã tạo câu hỏi chưa
                        if questionOfStudent == None:
                            questionOfExams = QuestionOfExam.objects.filter( exam_id = exam.id )
                            count = questionOfExams.count() -1
                            randomlist = []
                            
                            i = 0
                            while i < count:
                                
                                n = random.randint(0,count)
                                if checkIndex(randomlist,n) == None:
                                    i = i + 1
                                    randomlist.append(n)
                                    questionOfStudent = QuestionOfStudent()
                                    question =  questionOfExams[n].question
                                    questionOfStudent.exam = exam
                                    questionOfStudent.question = question
                                    questionOfStudent.student = student
                                    questionOfStudent.user = user
                                    questionOfStudent.save()
                                    
                                    choices = Choice.objects.filter( question_id = question.id )
                                
                                    countchoices = choices.count() -1
                                
                                    j = 0
                                    randomchoicelist = []
                                    while j < countchoices:
                                        m = random.randint(0,countchoices)
                                        if checkIndex(randomchoicelist,m) == None:
                                            j = j + 1
                                            randomchoicelist.append(m)
                                            choiceOfStudent = ChoiceOfStudent()
                                            choiceOfStudent.questionOfStudent = questionOfStudent
                                            choiceOfStudent.choice = choices[m].choice_name
                                            choiceOfStudent.save()
                            return redirect('quiz:quiz')
                        else:
                            
                            return redirect('quiz:quiz')
                    else:
                        # doing exam   
                            return redirect('quiz:quiz')


                #return HttpResponse("tạo đề thành công")
    ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##


    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    request.session['foo'] = 'bar'
    
    config = Configurations.objects.filter(id = 1).first()

    ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##
    totalStudents = Student.objects.count()
    totalTeachers = Teacher.objects.count()
    totalClasses = Class.objects.count()
    # loc các bài kiểm tra trong 1 tuần
    startdate = datetime.today() -timedelta(days=1)
    enddate = startdate + timedelta(days=6)
    #Sample.objects.filter(date__range=[startdate, enddate])
    #exams = Exam.objects.filter(start_date__range=["2021-06-01", "2021-06-30"])
    exams = Exam.objects.filter(start_date__range=[startdate, enddate]).order_by('start_date')
    #return HttpResponse(enddate)
    #exams = Exam.objects.all()
    return render(request, 'quiz/index.html',{
                                                'group':group ,
                                                'config':config,
                                                'totalStudents':totalStudents,
                                                'totalClasses':totalClasses,
                                                'totalTeachers':totalTeachers,
                                                'exams':exams,
                                                'Exam_types':Exam_type,
                                                'messages':messages
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)
def quiz(request):
    if request.session.get('check', True):
        #return HttpResponse("request.user.groups")
        question_list = QuestionOfStudent.objects.all()
        paginator = Paginator(question_list, 1) # Show 25 contacts per page.
        #ChoiceOfStudent
        page_number = request.GET.get('q')
        page_obj = paginator.get_page(page_number)
        return render(request, 'quiz/quiz.html', {'page_obj': page_obj})