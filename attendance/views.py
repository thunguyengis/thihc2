from django.http import HttpResponse
from django.shortcuts import render

from django.http import HttpResponseRedirect 
from django.core import serializers

from django.contrib.auth.decorators import login_required
from configurations.models import Configurations, Student, Teacher, Class, Course, CoursOfDepartment, CourseOfSection ,Grade, GradeOfVN, Section
from .models import Attendance
#rom django.utils import timezone
from datetime import datetime
# Create your views here.
def index(request):
 
    return render(request, 'attendance/index.html', {})

# vần còn lỗi khi điểm danh theo danh sách lơp hiện tại chứ khôgn phải theo khoá học
@login_required()
def course1(request, course_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
    myDate =  datetime.now().strftime ("%H:%M:%S %d/%m/%Y ")
    config = Configurations.objects.filter(id = 1).first()
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    teachers = Teacher.objects.filter(user_id = request.user.id).first()
    course = Course.objects.filter(id = course_id).first()
    #date = datetime.now().date()
    # loc điểm danh n=ngày hôm nay cau mon học
    attendances = Attendance.objects.filter(course_id = course_id, created_at__date = datetime.now().date())
    
   
    if request.method == 'POST':
        students_id = request.POST.getlist("students[]")
        #return HttpResponse(request.POST)
        for i, student_id in enumerate(students_id) :
            _i=str(i+1)
            int_present=0
            if 'isPresent'+_i in request.POST:
                present = request.POST['isPresent'+ _i ]
                if present=='on':
                    int_present=1
            addAttendanceoCourse(course_id,  int_present, student_id , request.user.id )
    # danh sách học viên
    students = Student.objects.filter(myclass_id = course.section.myclass_id)
    # kiểm tra 
    #attendances_att = Attendance.objects.filter(course_id = course_id)     
    attCount = []    
    if  students :          
        for i, student in enumerate(students) :
            at = dict()
            at['student_id'] = student.id
            at['totalPresent'] = Attendance.objects.filter(course_id = course_id).filter(present = 1).filter(student_id = student.id).count()
            at['totalAbsent'] = Attendance.objects.filter(course_id = course_id).filter(present = 0).filter(student_id = student.id).count()
            at['totalEscaped'] = Attendance.objects.filter(course_id = course_id).filter(present = 2).filter(student_id = student.id).count()
            attCount.append(at)
    #return HttpResponse(attCount)
    return render(request, 'attendance/attendance.html',{
                                                'group':group ,
                                                'config':config,
                                                'myDate':myDate,
                                                'attendances': attendances,
                                               # 'attendances_date':attendances_date,
                                                'course':course,
                                                'teachers':teachers,
                                                'students':students,
                                                'attCount':attCount
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)
# vđiểm danh theo  khoá học
@login_required()
def course(request, course_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
    myDate =  datetime.now().strftime ("%H:%M:%S %d/%m/%Y ")
    config = Configurations.objects.filter(id = 1).first()
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    teachers = Teacher.objects.filter(user_id = request.user.id).first()
    course = CourseOfSection.objects.filter(id = course_id).first()
    #return HttpResponse(course)
    #date = datetime.now().date()
    # loc điểm danh n=ngày hôm nay cau mon học
    attendances = Attendance.objects.filter(course_id = course_id, created_at__date = datetime.now().date())
  
   
    if request.method == 'POST':
        students_id = request.POST.getlist("students[]")
        #return HttpResponse(request.POST)
        for i, student_id in enumerate(students_id) :
            _i=str(i+1)
            int_present=0
            if 'isPresent'+_i in request.POST:
                present = request.POST['isPresent'+ _i ]
                if present=='on':
                    int_present=1
            addAttendanceoCourse(course_id,  int_present, student_id , request.user.id )
    # danh sách học viên
    students = Student.objects.filter(myclass_id = course.section.myclass_id)
    # kiểm tra 
    #attendances_att = Attendance.objects.filter(course_id = course_id)     
    attCount = []    
    if  students :          
        for i, student in enumerate(students) :
            at = dict()
            at['student_id'] = student.id
            at['totalPresent'] = Attendance.objects.filter(course_id = course_id).filter(present = 1).filter(student_id = student.id).count()
            at['totalAbsent'] = Attendance.objects.filter(course_id = course_id).filter(present = 0).filter(student_id = student.id).count()
            at['totalEscaped'] = Attendance.objects.filter(course_id = course_id).filter(present = 2).filter(student_id = student.id).count()
            attCount.append(at)
    #return HttpResponse(attCount)
    grades = GradeOfVN.objects.filter(courseOfSection_id = course_id)
    return render(request, 'attendance/attendance.html',{
                                                'group':group ,
                                                'config':config,
                                                'myDate':myDate,
                                                'attendances': attendances,
                                               # 'attendances_date':attendances_date,
                                                'course':course,
                                                'teachers':teachers,
                                                'students':students,
                                                'attCount':attCount,
                                                'grades':grades
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)

# hàm đẻ thêm grade sau khi thêm course
def addAttendanceoCourse(course_id, present, student_id , user_id):
    item = Attendance()
    item.course_id =  course_id
    item.present = present
    item.student_id = student_id
    item.user_id = user_id   
    item.save()

def student(request):
    classes = Class.objects.all
    sections = Section.objects.all
    courses = CourseOfSection.objects.all
    #return HttpResponse(sections)
    return render(request, 'attendance/section-attendances.html', {
                                                'classes':classes,
                                                'sections':sections,
                                                'courses':courses,
                                    
                                            })

def listofstudent(request, course_id):
    classes = Class.objects.all
    sections = Section.objects.all
    courses = CourseOfSection.objects.all
    mytype='student'
    course = CourseOfSection.objects.filter(id = course_id).first()
    students = Student.objects.filter(myclass_id = course.section.myclass_id)
    #return HttpResponse(sections)
    return render(request, 'list/student-list-attendance.html', {
                                                'classes':classes,
                                                'sections':sections,
                                                'courses':courses,
                                                'users':students,
                                                'type':mytype,
                                                'course_id':course_id
                                    
                                            })
import json
def student_details(request, student_id, course_id):
    classes = Class.objects.all
    sections = Section.objects.all
    courses = Course.objects.all
    student = Student.objects.filter( id=student_id).first()
    mytype='student'
    attendances = Attendance.objects.filter(course_id = course_id, student_id=student_id)#[:2]

    #course = Course.objects.filter(id = course_id).first()
    #students = Student.objects.filter(myclass_id = course.section.myclass_id)
    #return HttpResponse(attendances)
    events = []    
    for attendance in attendances :
        at = dict()
        at["start"] = attendance.created_at.strftime ("%Y-%m-%dT%H:%M:%S") #"Apr 06 2021 10:58:01pm" #
        at["end"] = attendance.updated_at.strftime ("%Y-%m-%dT%H:%M:%S") #"Apr 06 2021 10:58:01pm" #
        if attendance.present == 1:
            at["title"] = "Present"            
            at["color"] = "green"
        elif  attendance.present == 2:
            at["title"] = "Present"   
            at["color"] = "orange"          
            
        else :
            at["title"] = "Present" 
            at["color"] = "red"           
           
        events.append(at)
        
    #data = serializers.serialize('json', events)
    #return HttpResponse(json.dumps(events))
    return render(request, 'attendance/student-attendances.html', {
                                                'classes':classes,
                                                'attendances':attendances,
                                                'events':json.dumps(events),
                                                'student':student,
                                                #'users':students,
                                                'type':mytype
                                    
                                            })

