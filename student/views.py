from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
#
from configurations.models import Class, Configurations, Course, Student
#import openpyxl
import openpyxl

# Create your views here.
@login_required()
def sectionStudent(request, section_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    courses = Course.objects.filter(section_id = section_id)
    #return HttpResponse(courses)
    return render(request, 'student/section-students.html',{
                                                'group':group ,
                                                'config':config,
                                                
                                             })
@login_required()
def classStudent(request, class_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    #courses = Course.objects.filter(section_id = section_id)
    #return HttpResponse(courses)
    myclass = Class.objects.filter(id = class_id).first()
    students = Student.objects.filter(myclass_id = class_id)
    return render(request, 'student/class-students.html',{
                                                'group':group ,
                                                'config':config,
                                                'users':students,
                                                'class':myclass
                                                
                                             })

@login_required()
def importStudent(request):
    if "POST" == request.method:
        
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        #print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        i = 0
        for row in worksheet.iter_rows():
            row_data = list()
            if i!=0:
               
                myclass = Class.objects.filter(class_name = str(row[0].value)).first()
                if myclass:
                    try:
                        user  =  User()
                        user.username = row[1].value
                        user.first_name = row[2].value
                        user.last_name = row[3].value
                        user.password = make_password('123456')
                        user.save()
                        
                        #form
                    except:
                        return HttpResponseRedirect(reverse('configurations:configurations'))
 
                    student = Student()
                    student.user = user
                    student.myclass_id = myclass.id
                    student.birthday = row[4].value
                    student.religion = row[5].value
                    student.gender = row[6].value
                    student.save()
            i = i +1

    return HttpResponseRedirect(reverse('configurations:configurations'))
 