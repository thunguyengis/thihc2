
from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponseRedirect 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from configurations.models import Configurations, Student, Teacher, Class
from question.models import QuestionOfExam

from exam.views import Exam_type
from exam.models import Exam
from datetime import datetime, date, timedelta

# thông báo lỗi
from django.contrib import messages 


def index(request):
     #lưu dữ liệu 
    if request.method == 'POST':
        #return HttpResponse("exam")
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
                #return HttpResponse(exam.getClass())
                if student.myclass.id == exam.getClass():
                    questionOfExam = QuestionOfExam.objects.filter( exam_id = exam.id ).get()
                    return HttpResponse(questionOfExam)

                
       
        
       

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