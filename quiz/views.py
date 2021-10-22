
from math import e
from django.db.models.enums import Choices
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.http import HttpResponseRedirect 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from configurations.models import Configurations, GradeOfVN, Student, Teacher, Class
from question.models import QuestionOfExam, Choice, Question
from exam.views import Exam_type
from exam.models import Exam, GradeOfExam
from .models import QuestionOfStudent, ChoiceOfStudent

from datetime import datetime, date, timedelta

# thông báo lỗi
from django.contrib import messages 
import random
#Paginator
from django.core.paginator import Paginator
#
import math

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
                    request.session['student_id'] = student.id 
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
                            while i <= count:
                                
                                n = random.randint(0,count)
                                if checkIndex(randomlist,n) == None:
                                    i = i + 1
                                    randomlist.append(n)
                                    questionOfStudent = QuestionOfStudent()
                                    question =  questionOfExams[n].question
                                    questionOfStudent.exam = exam
                                    questionOfStudent.question = question
                                    questionOfStudent.question_content = question.question_name
                                    questionOfStudent.question_type = question.question_type
                                    questionOfStudent.correct_answer = question.correct_answer
                                    questionOfStudent.student = student
                                    questionOfStudent.user = user
                                    questionOfStudent.save()
                                    
                                    choices = Choice.objects.filter( question_id = question.id )
                                
                                    countchoices = choices.count() -1
                                
                                    j = 0
                                    randomchoicelist = []
                                    while j <= countchoices:
                                        m = random.randint(0,countchoices)
                                        if checkIndex(randomchoicelist,m) == None:
                                            j = j + 1
                                            randomchoicelist.append(m)
                                            choiceOfStudent = ChoiceOfStudent()
                                            choiceOfStudent.questionOfStudent = questionOfStudent
                                            choiceOfStudent.choice = choices[m].choice_name
                                            choiceOfStudent.save()
                            return redirect('quiz:check')
                        else:
                            
                            return redirect('quiz:check')
                    else:
                        # doing exam   
                            return redirect('quiz:check')


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
def check(request):
   
    if request.session.get('check') != None:
        if request.session.get('check', True):
        
            exam_code = request.session.get('exam_code')
            exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            student = Student.objects.filter(id = student_id).first()

            #return HttpResponse(  icorrect/question_list.count() ) 
            ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##
            grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
            mark = grade.mark

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
            return render(request, 'quiz/check.html',{
                                                    'group':group ,
                                                    'config':config,
                                                    'totalStudents':totalStudents,
                                                    'totalClasses':totalClasses,
                                                    'totalTeachers':totalTeachers,
                                                    'student':student,
                                                    'exam':exam,
                                                    'mark':mark,
                                                    'Exam_types':Exam_type,
                                                    'messages':messages
                                                })         
    return redirect('quiz:index')
def quiz(request):
    #return HttpResponse(request.POST)
    
    if request.session.get('check') != None:
        if  request.session.get('check', True):
            #return HttpResponse("request.user.groups")
            #question_list = QuestionOfStudent.objects.all()
            exam_code = request.session.get('exam_code')
            exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            question_list = QuestionOfStudent.objects.filter( exam_id = exam.id,student_id = student_id)
            grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
            time_remaining = int (grade.time_remaining)
            if 'time_second' in request.POST :
                second = request.POST['time_second']
            
                time_remaining =  time_remaining + int(second)  - time_remaining%60 + 1
                grade.doing_exam = True
                grade.time_remaining =    time_remaining
                grade.save()                                 
            #---------------------------------------------------
            #
            if 'qcurent' in request.POST and question_list.count() != 0 :
                qcurent = request.POST['qcurent']
                    # cập nhật cấu trả lời
                
                question_prev = question_list[int(qcurent) -1]
                if 'answers[]' in request.POST :
                    answers = request.POST.getlist("answers[]")
                    correct_answers = ""
                    for i, item in enumerate(answers):
                        correct_answers = correct_answers + item
                    question_prev.choice = correct_answers
                    question_prev.save()
                    
            if 'type' in request.POST and request.POST['type']=='review' :
                if 'qcurent' in request.POST :
                        qcurent = request.POST['qcurent']
                        return HttpResponseRedirect('review/' + str(qcurent ))
            if 'type' in request.POST and request.POST['type']=='point' :
                if 'qcurent' in request.POST :
                        qcurent = request.POST['qcurent']
                        return HttpResponseRedirect('point/' + str(qcurent ))
            #---------------------------------------------------                                                    
            paginator = Paginator(question_list, 1) # Show 25 contacts per page.
            #ChoiceOfStudent
            page_number=None
            if 'q' in request.GET :
                page_number = request.GET.get('q')
            if 'q' in request.POST :
                page_number = request.POST['q']
            #return HttpResponse(page_number)
            #page_number = request.GET.get('q')
            #return HttpResponse(page_number)
            page_obj = paginator.get_page(page_number)
            choices = None
            question_choice = None
            
            if page_number == None and question_list.count() != 0:
                question = question_list[0]
                question_choice = question.choice
                choices = ChoiceOfStudent.objects.filter(questionOfStudent_id = question.id )
                
            elif question_list.count() != 0:
                #return HttpResponse(request.POST)
            
                
                question = question_list[int(page_number)-1]
                question_choice = question.choice
                choices = ChoiceOfStudent.objects.filter(questionOfStudent_id = question.id )
        

            minute = time_remaining//60
            second = time_remaining%60
            return render(request, 'quiz/quiz.html', {'page_obj': page_obj,
                                                    'question':question,
                                                    'choices':choices,
                                                    'question_choice': question_choice,
                                                    'exam': exam,
                                                    'minute':minute,
                                                    'second':second,
                                                    'time_exam': exam.time_exam })
    return redirect('quiz:index')
def review(request, c):
    if request.session.get('check') != None:
        if request.session.get('check', True):
        
            exam_code = request.session.get('exam_code')
            exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            question_list = QuestionOfStudent.objects.filter( exam_id = exam.id, student_id = student_id)
            grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
            time_remaining = int (grade.time_remaining)
            minute = time_remaining//60
            second = time_remaining%60

            return render(request, 'quiz/review.html', {'question_list':question_list,
                                                        'minute':minute,
                                                        'second':second})
    return redirect('quiz:index')
def time(request):
    if request.session.get('check') != None:
        if request.session.get('check', True):
        
            exam_code = request.session.get('exam_code')
            exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            
            
            grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
            grade.time_remaining = int( grade.time_remaining ) + 60
            grade.save()
            return HttpResponse('1')
    return redirect('quiz:index')
def timesecond(request):
    if request.session.get('check') != None:
        if request.session.get('check', True):
        
            exam_code = request.session.get('exam_code')
            exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            
            
            grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
            grade.time_remaining = int( grade.time_remaining ) + 1
            grade.save()
            return HttpResponse('1')  
    return redirect('quiz:index')
def diem(request, c):
    if request.session.get('check') != None:
        if request.session.get('check', True):
        
            exam_code = request.session.get('exam_code')
            exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            question_list =QuestionOfStudent.objects.filter( exam_id = exam.id, student_id = student_id)
            
            icorrect=0
            for item in question_list:
                q = Question.objects.filter( id = item.question_id).first()
                #return HttpResponse(q.correct_answer)
                if q.correct_answer == item.choice:
                    icorrect = icorrect + 1
                
            # điểm theo buổi thi
            grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
            mark = None
            if question_list.count() != 0:
                mark = round( icorrect*10/question_list.count(), 2) 
                grade.mark = mark
                grade.save()
            # cập nhật điểm theo môn học
            gradeOfVN = GradeOfVN.objects.filter( student_id=student_id, courseOfSection_id = exam.courseOfSection_id ).first()
            #return HttpResponse( exam.courseOfSection_id)
            if gradeOfVN !=None and mark != None:
                if exam.exam_type2 == 'coefficient_1_1':
                    gradeOfVN.coefficient_1_1 =mark
                    
                elif exam.exam_type2 == 'coefficient_1_2':
                    gradeOfVN.coefficient_1_2 =mark
                elif exam.exam_type2 == 'coefficient_2_1':
                    gradeOfVN.coefficient_2_1 =mark
                elif exam.exam_type2 == 'coefficient_2_2':
                    gradeOfVN.coefficient_2_2 =mark
                elif exam.exam_type2 == 'end_mark_1_1':
                    gradeOfVN.end_mark_1_1 =mark
                elif exam.exam_type2 == 'coefficient_v2_1_1': 
                    gradeOfVN.coefficient_v2_1_1 =mark
                elif exam.exam_type2 == 'coefficient_v2_1_2':
                    gradeOfVN.coefficient_v2_1_2 =mark
                elif exam.exam_type2 == 'coefficient_v2_2_1':
                    gradeOfVN.coefficient_v2_2_1 =mark
                elif exam.exam_type2 == 'coefficient_v2_2_2': 
                    gradeOfVN.coefficient_v2_2_2 =mark
                elif exam.exam_type2 == 'end_mark_v2_1_1':
                    gradeOfVN.end_mark_v2_1_1 =mark
                elif exam.exam_type2 == 'practical_1_1': 
                    gradeOfVN.practical_1_1 =mark
                else:
                    gradeOfVN.practical_v2_1_1 =mark

                gradeOfVN.save()
            # hiên thị điểm
           # exam_code = request.session.get('exam_code')
           # exam = Exam.objects.filter(exam_code = exam_code).first()
            student_id = request.session.get('student_id')
            student = Student.objects.filter(id = student_id).first()

            #return HttpResponse(  icorrect/question_list.count() ) 
            ##%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%##
            #grade = GradeOfExam.objects.filter( exam_id = exam.id,student_id = student_id).first()
           # mark = grade.mark

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

            request.session['check'] = None
            request.session['username'] = None
            request.session['exam_code'] = None
            request.session['student_id'] = None
            return render(request, 'quiz/check.html',{
                                                    'group':group ,
                                                    'config':config,
                                                    'totalStudents':totalStudents,
                                                    'totalClasses':totalClasses,
                                                    'totalTeachers':totalTeachers,
                                                    'student':student,
                                                    'exam':exam,
                                                    'mark':mark,
                                                    'Exam_types':Exam_type,
                                                    'messages':messages
                                                })                                                          
    return redirect('quiz:index')