from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
#
from configurations.models import Class, Configurations, Course, Section, Student, Teacher, Grade, CourseOfSection, GradeOfVN
from exam.views import Exam_type
# thông báo lỗi
from django.contrib import messages 
# Create your views here.
@login_required()
def CourseOfTeacher(request, course_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    grades = GradeOfVN.objects.filter(courseOfSection_id = course_id)
    course = CourseOfSection.objects.filter(id = course_id).first()
   
    #messages.error(request, "Mã Học viên đã tồn tại")
    return render(request, 'grade/course-grade.html',{
                                                'group':group ,
                                                'config':config,
                                                'grades':grades,
                                                'course': course,
                                                'Exam_types':Exam_type,
                                             })

#################################################################################################
#
#           XỬ LÝ ĐIỂM
#
#################################################################################################
def total_mark_exam(countHS1, totalHS1, countHS2, totalHS2):
    #return HttpResponse((totalHS1 + totalHS2*2))
    mark_exam = (totalHS1 + totalHS2*2)/(countHS1 + countHS2*2 )
    return round(mark_exam,2)
def total_mark_course(mark_exam, totalEnd):
    mark_course = mark_exam * 0.4 + totalEnd * 0.6
    return round(mark_course,2)
@login_required()
def update(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(request.POST)
    if request.method == 'POST':
        config = Configurations.objects.filter(id = 1).first()
        teacher = Teacher.objects.filter(user_id = request.user.id).first() 
        courses = Course.objects.filter(teacher_id = teacher.id)
        #grades = Grade.objects.filter(course_id = course_id)
        grade_ids = request.POST.getlist("grade_id[]")
        if 'course_id' in request.POST:
            course_id = request.POST['course_id'] 
        '''
        attendance = request.POST.getlist("attendance[]")
        quiz1 = request.POST.getlist("quiz1[]")
        quiz2 = request.POST.getlist("quiz2[]")
        quiz3 = request.POST.getlist("quiz3[]")
        quiz4 = request.POST.getlist("quiz4[]")
        quiz5 = request.POST.getlist("quiz5[]")
        ct1 = request.POST.getlist("ct1[]")
        ct2 = request.POST.getlist("ct2[]")
        ct3 = request.POST.getlist("ct3[]")
        ct4 = request.POST.getlist("ct4[]")
        ct5 = request.POST.getlist("ct5[]")
        assignment1 = request.POST.getlist("assignment1[]")
        assignment2 = request.POST.getlist("assignment2[]")
        assignment3 = request.POST.getlist("assignment3[]")
        written = request.POST.getlist("written[]")
        mcq = request.POST.getlist("mcq[]")
        practical = request.POST.getlist("practical[]")
        '''
        
        coefficient_1_1 = request.POST.getlist("coefficient_1_1[]")
        coefficient_1_2 = request.POST.getlist("coefficient_1_2[]")
        coefficient_2_1 = request.POST.getlist("coefficient_2_1[]")
        coefficient_2_2 = request.POST.getlist("coefficient_2_2[]")
        coefficient_v2_1_1 = request.POST.getlist("coefficient_v2_1_1[]")
        coefficient_v2_1_2 = request.POST.getlist("coefficient_v2_1_2[]")
        coefficient_v2_2_1 = request.POST.getlist("coefficient_v2_2_1[]")
        coefficient_v2_2_2 = request.POST.getlist("coefficient_v2_2_2[]")
        
        end_mark_1_1 = request.POST.getlist("end_mark_1_1[]")
        end_mark_v2_1_1 = request.POST.getlist("end_mark_v2_1_1[]")
        practical_1_1 = request.POST.getlist("practical_1_1[]")
        practical_v2_1_1 = request.POST.getlist("practical_v2_1_1[]")

       

        for key, value in enumerate( grade_ids) :
            i = int(key) 
            countHS1 = 0
            countHS2 = 0
            totalHS1 = 0
            totalHS2 = 0
            totalEnd = 0
            grade = GradeOfVN.objects.filter( id = value).first()  
            if float( coefficient_1_1[i]) > 0:
                countHS1 = countHS1 + 1
                totalHS1 = totalHS1 + float(coefficient_1_1[i])
                
                grade.coefficient_1_1 = coefficient_1_1[i]
            if float(coefficient_1_2[i]) > 0:
                countHS1 = countHS1 + 1
                totalHS1 = totalHS1 + float(coefficient_1_2[i])
                
                grade.coefficient_1_2 = coefficient_1_2[i]

            if float(coefficient_2_1[i]) > 0:
                countHS2 = countHS2 + 1
                totalHS2 = totalHS2 + float(coefficient_2_1[i])
                grade.coefficient_2_1 = coefficient_2_1[i]
            if float(coefficient_2_2[i]) > 0:
                countHS2 = countHS2 + 1
                totalHS2 = totalHS2 + float(coefficient_2_2[i])
                grade.coefficient_2_2 = coefficient_2_2[i]

              # thi lại điêmt hệ số 1
            if float(coefficient_v2_1_1[i]) > 0:
                countHS1 = 0
                totalHS1 = 0
                countHS1 = countHS1 + 1
                totalHS1 = totalHS1 + float(coefficient_v2_1_1[i])
               
                grade.coefficient_v2_1_1 = coefficient_v2_1_1[i]
            
            if float(coefficient_v2_1_2[i]) > 0:
                countHS1 = countHS1 + 1
                totalHS1 = totalHS1 + float(coefficient_v2_1_2[i])
                
                grade.coefficient_v2_1_2 = coefficient_v2_1_2[i]
            # thi lại điêmt hệ số 2
            if float(coefficient_v2_2_1[i]) > 0:
                countHS2 = 0
                totalHS2 = 0
                countHS2 = countHS2 + 1
                totalHS2 = totalHS2 + float(coefficient_v2_2_1[i])
                grade.coefficient_v2_2_1 = coefficient_v2_2_1[i]
            if float(coefficient_v2_2_2[i]) > 0:
                countHS2 = countHS2 + 1
                totalHS2 = totalHS2 + float(coefficient_v2_2_2[i])
                grade.coefficient_v2_2_2 = coefficient_v2_2_2[i]

    
            # 
            if float(end_mark_1_1[i]) > 0:
                totalEnd = float(end_mark_1_1[i])
                grade.end_mark_1_1 = end_mark_1_1[i]
            if float(end_mark_v2_1_1[i]) > 0:
                totalEnd = float(end_mark_v2_1_1[i])
                grade.end_mark_v2_1_1 = end_mark_v2_1_1[i]

            grade.practical_1_1 = practical_1_1[i]
            grade.practical_v2_1_1 = practical_v2_1_1[i]
            
            if countHS1>0 and  countHS2 >0 :

                mark_exam = total_mark_exam(countHS1, totalHS1, countHS2, totalHS2)
                #return HttpResponse(mark_exam)
                grade.total_mark_exam =  mark_exam
                if mark_exam>5 :
                    grade.total_mark_course = total_mark_course(mark_exam, totalEnd)
                    
           
            grade.save()
      
    return redirect('grade:courseOfTeacher', course_id=course_id)
    

###########################################################################################
#
## view điểm
#
###########################################################################################
def allExamsGrade(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    
    classes = Class.objects.all()
    sections = Section.objects.all()
    return render(request, 'grade/all-exams-grade.html',{
                                                'group':group ,
                                                'config':config,
                                                'classes':classes,
                                                'sections':sections
                                               
                                             }) 

def gradesOfSection(request, section_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    
    config = Configurations.objects.filter(id = 1).first()
    
    classes = Class.objects.all()
    sections = Section.objects.all()
    return render(request, 'grade/class-result.html',{
                                                'group':group ,
                                                'config':config,
                                                'classes':classes,
                                                'sections':sections
                                               
                                             }) 
def gradesOfCourse(request, course_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    
    classes = Class.objects.all()
    sections = Section.objects.all()
    return render(request, 'grade/class-result.html',{
                                                'group':group ,
                                                'config':config,
                                                'classes':classes,
                                                'sections':sections
                                             }) 
def marks(request, course_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    
    classes = Class.objects.all()
    sections = Section.objects.all()
    grades = GradeOfVN.objects.filter(courseOfSection_id = course_id)
    #return HttpResponse(grades)
    #for g in grades:
    #    return HttpResponse(g.coefficient_2_1 != -1.0)
    return render(request, 'grade/teacher-grade.html',{
                                                'group':group ,
                                                'config':config,
                                                'grades':grades,
                                                'Exam_types':Exam_type,
                                                'set0':-1.0
                                               
                                             }) 

def history(request, student_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    
    classes = Class.objects.all()
    sections = Section.objects.all()
    student = Student.objects.filter( id = student_id).first()
    grades = GradeOfVN.objects.filter(student_id = student_id)

    #exams = 
    #for g in grades:
    #    return HttpResponse(g.coefficient_2_1 != -1.0)
    return render(request, 'grade/student-grade.html',{
                                                'group':group ,
                                                'config':config,
                                                'grades':grades,
                                                'Exam_types':Exam_type,
                                                'set0':-1.0,
                                                'student':student
                                               
                                             }) 