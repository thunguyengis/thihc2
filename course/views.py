from django.http import HttpResponse, JsonResponse
from django.shortcuts import render


from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from configurations.models import Grade, Section
#
from configurations.models import Configurations, Course, Teacher, CourseOfSection
# Create your views here.
@login_required()
@permission_required('course.index', raise_exception=True)
def index(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    classes = Class.objects.all()
    formClass2 = ClassForm()
    sections = Section.objects.all()
    formSection = SectionForm()
    formCourse = CourseForm()
    return render(request, 'configurations/index.html',{
                                                'group':group ,
                                                'config':config,
                                                'classes':classes,
                                                'formClass':formClass2,
                                                'sections':sections,
                                                'formSection':formSection,
                                                'formCourse':formCourse,
                                             })

@login_required()
@permission_required('course.section', raise_exception=True)
def section(request, section_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    section = Section.objects.filter(id = section_id).first()
    courses = CourseOfSection.objects.filter(section_id = section_id)
    #return HttpResponse(courses)
    return render(request, 'course/class-course.html',{
                                                'group':group ,
                                                'config':config,
                                                'mycourses': courses,
                                                'section':section
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)

@login_required()
@permission_required('course.teacher', raise_exception=True)
def teacher(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    teacher = Teacher.objects.filter(user_id = request.user.id).first()
    courses = CourseOfSection.objects.filter(teacher_id = teacher.id)
    #return HttpResponse(courses)
    return render(request, 'course/teacher-course.html',{
                                                'group':group ,
                                                'config':config,
                                                'teacher':teacher,
                                                'mycourses': courses,
                                             })

