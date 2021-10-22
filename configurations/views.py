from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User

from .models import Configurations, Department , Student    #, UserForm
from .models import Teacher, Class, Section, Course, Grade, GradeOfVN, CourseOfSection, CoursOfDepartment
# Create your views here.
#form
from .forms import TeacherForm, SectionForm, CourseForm, CourseOfSectionForm, StudentForm, ClassForm

# thông báo lỗi
from django.contrib import messages 

# để luu file về server
from django.core.files.storage import FileSystemStorage
# Imaginary function to handle an uploaded file.
#from somewhere import handle_uploaded_file
# Xóa dấu tiếng việt trong Python
import unidecode
import re
#@login_required(redirect_field_name="/polls/3")
@login_required()
@permission_required('configurations.configurations', raise_exception=True)
@login_required()
def index(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    classes = Class.objects.all()
    departments = Department.objects.all()
    coursOfDepartments = CoursOfDepartment.objects.all()
    formClass2 = ClassForm()
    sections = Section.objects.all()
    formSection = SectionForm()
    formCourse = CourseOfSectionForm()
    return render(request, 'configurations/index.html',{
                                                'group':group ,
                                                'config':config,
                                                'classes':classes,
                                                'departments':departments,
                                                'coursOfDepartments': coursOfDepartments,
                                                'formClass':formClass2,
                                                'sections':sections,
                                                'formSection':formSection,
                                                'formCourse':formCourse,
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)
@login_required()
def classes(request):
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
    formCourse = CourseOfSection()
    #return HttpResponse(sections)
    return render(request, 'configurations/classes.html',{
                                                'group':group ,
                                                'config':config,
                                                'classes':classes,
                                                'sections':sections,
                                             })
@login_required()
def departments(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    list_departments = []
    departments = Department.objects.all()
    for dep in departments:
        teacher = Teacher.objects.filter(department_id = dep.id).first()
        if teacher != None:
            list_departments.append(dep)
    teachers = Teacher.objects.all()
    #return HttpResponse(sections)
    return render(request, 'configurations/departments.html',{
                                                'group':group ,
                                                'config':config,
                                                'departments':list_departments,
                                                'teachers':teachers,
                                             })
 
 
#
@login_required()
def addDepartment(request):
    #department_name
    if request.method == 'POST':
        department = Department()
        department.department_name = request.POST['department_name']
        department.save()
    return HttpResponseRedirect(reverse('configurations:configurations'))

@login_required()
def addCourseOfDepartment(request):
    #department_name
    if request.method == 'POST':
        department = CoursOfDepartment()
        department.department_id = request.POST['department']
        department.course_name = request.POST['course_name']
        department.save()
    return HttpResponseRedirect(reverse('configurations:configurations'))
###################################################################################
 
def no_accent_vietnamese(s):
    s = re.sub('[áàảãạăắằẳẵặâấầẩẫậ]', 'a', s)
    s = re.sub('[ÁÀẢÃẠĂẮẰẲẴẶÂẤẦẨẪẬ]', 'A', s)
    s = re.sub('[éèẻẽẹêếềểễệ]', 'e', s)
    s = re.sub('[ÉÈẺẼẸÊẾỀỂỄỆ]', 'E', s)
    s = re.sub('[óòỏõọôốồổỗộơớờởỡợ]', 'o', s)
    s = re.sub('[ÓÒỎÕỌÔỐỒỔỖỘƠỚỜỞỠỢ]', 'O', s)
    s = re.sub('[íìỉĩị]', 'i', s)
    s = re.sub('[ÍÌỈĨỊ]', 'I', s)
    s = re.sub('[úùủũụưứừửữự]', 'u', s)
    s = re.sub('[ÚÙỦŨỤƯỨỪỬỮỰ]', 'U', s)
    s = re.sub('[ýỳỷỹỵ]', 'y', s)
    s = re.sub('[ÝỲỶỸỴ]', 'Y', s)
    s = re.sub('đ', 'd', s)
    s = re.sub('Đ', 'D', s)
    return s
@login_required()
def add_student(request):
    # if this is a POST request we need to process the form data
    config = Configurations.objects.filter(id = 1).first()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
         # create object of form 
        #form = StudentForm(request.POST or None, request.FILES or None) 
         # create a form instance and populate it with data from the request:
        form = StudentForm(request.POST, request.FILES) 
        # check whether it's valid:
        form.is_valid()
        
        try:
            user  =  User()
            user.username = form.cleaned_data['code_student']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.password ='123456'
            user.save()
             
            #form
        except:
             messages.error(request, "Mã Học viên đã tồn tại")

        
       # if the post request has a file under the input name 'document', then save the file. 
        request_file = request.FILES['picpath'] if 'picpath' in request.FILES else None
        if request_file: 
            # save attatched file 
    
            # create a new instance of FileSystemStorage 
            fs = FileSystemStorage() 
            file = fs.save(  unidecode.unidecode(request_file.name),  request_file) 
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
            fileurl = fs.url(file) 
            sudent = Student()
            sudent.user_id = user.id
            sudent.myclass_id = request.POST['myclass']
            sudent.birthday = form.cleaned_data['birthday']
            sudent.religion = form.cleaned_data['religion']
            sudent.picpath = fileurl
            sudent.gender = form.cleaned_data['gender']
            sudent.save()
            return HttpResponseRedirect(reverse('configurations:configurations'))
        else:        
            messages.error(request, request.POST['myclass'] )           
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

        #return HttpResponse(form.cleaned_data['picpath'])
        
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})
        
        #return HttpResponse(form.cleaned_data['username'])
    # if a GET (or any other method) we'll create a blank form
    else:
      
        form = StudentForm()
        #formuser = UserForm()

        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})

#
@login_required()
def add_class(request):
    
    # if this is a POST request we need to process the form data
    config = Configurations.objects.filter(id = 1).first()
    if request.method == 'POST':
        form = ClassForm(request.POST)
       
        # check whether it's valid:
        if form.is_valid(): 
            form.save()
        
        return HttpResponseRedirect(reverse('configurations:configurations'))
    # if a GET (or any other method) we'll create a blank form
    else: 
        form = ClassForm()
        #formuser = UserForm()
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})

#
@login_required()
def add_section(request):
    # if this is a POST request we need to process the form data
    config = Configurations.objects.filter(id = 1).first()
    if request.method == 'POST':
        section = Section()
        section.section_name = request.POST['section_name']
        section.myclass_id = request.POST['myclass']
        section.user_id = request.user.id
        #section.myclass_id = request.POST['myclass']
        section.save()
        return HttpResponseRedirect(reverse('configurations:configurations'))
    # if a GET (or any other method) we'll create a blank form
    else: 
        form = SectionForm()
        #formuser = UserForm()
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})

#
@login_required()
def add_course_goc(request):
    # if this is a POST request we need to process the form data
   
    config = Configurations.objects.filter(id = 1).first()
    form = CourseForm(request.POST) 
    if  form.is_valid():
        item = Course()
        item.course_name = form.cleaned_data['course_name']
        item.teacher_id = request.POST['teacher']
        item.course_time = form.cleaned_data['course_time']
        item.section_id = request.POST['section_id'] 
        item.user_id = request.user.id
        item.save()
        
        myclass = Class.objects.filter(section = item.section_id ).first()
        students =  Student.objects.filter(myclass_id = myclass.id)
        for student in students :
            addGradeToCourse(item.id, item.teacher_id, student.id, item.user_id )
        return render(request, 'configurations/index.html', { 'config': config})
    # if a GET (or any other method) we'll create a blank form
    else: 
        #form = SectionForm()
        #formuser = UserForm()
        return render(request, 'configurations/index.html', {'form': form,  'config': config})

#@login_required()
def add_course(request):
    # if this is a POST request we need to process the form data
   
    config = Configurations.objects.filter(id = 1).first()
    form = CourseOfSectionForm(request.POST) 
    if  form.is_valid():
        item = CourseOfSection()
        
        item.coursOfDepartment_id = request.POST['coursOfDepartment']
        item.teacher_id = request.POST['teacher']
        item.course_time = form.cleaned_data['course_time']
        item.section_id = request.POST['section_id'] 
        item.user_id = request.user.id
        item.save()
        
        myclass = Class.objects.filter(section = item.section_id ).first()
        students =  Student.objects.filter(myclass_id = myclass.id)
        for student in students :
            addGradeToCourseVN(item.id, item.teacher_id, student.id, item.user_id )
        return HttpResponseRedirect(reverse('configurations:configurations'))
    # if a GET (or any other method) we'll create a blank form
    else: 
        #form = SectionForm()
        #formuser = UserForm()
        return render(request, 'configurations/index.html', {'form': form,  'config': config})

# hàm tụe động thêm vào
# hàm đẻ thêm grade sau khi thêm course
def addGradeToCourse(course_id, teacher_id, student_id , user_id):
    grade = Grade()
    grade.course_id =  course_id
    grade.teacher_id = teacher_id
    grade.student_id = student_id
    grade.user_id = user_id   
    grade.save()
def addGradeToCourseVN(course_id, teacher_id, student_id , user_id):
    grade = GradeOfVN()
    grade.courseOfSection_id =  course_id
    grade.teacher_id = teacher_id
    grade.student_id = student_id
    grade.user_id = user_id   
    grade.save()
#
@login_required()
def add_teacher(request):
       # if this is a POST request we need to process the form data
    config = Configurations.objects.filter(id = 1).first()
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
         # create object of form 
        #form = StudentForm(request.POST or None, request.FILES or None) 
         # create a form instance and populate it with data from the request:
        form = TeacherForm(request.POST, request.FILES) 
        # check whether it's valid:
        form.is_valid()
        
        try:
            user  =  User()
            user.username = form.cleaned_data['code_teacher']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.password ='123456'
            user.save()
           
            #form
        except:
             messages.error(request, "Mã Học viên đã tồn tại")

        
       # if the post request has a file under the input name 'document', then save the file. 
        request_file = request.FILES['picpath'] if 'picpath' in request.FILES else None
        
        if request_file:
            # create a new instance of FileSystemStorage 
            fs = FileSystemStorage() 
            file = fs.save(request_file.name, request_file) 
            # the fileurl variable now contains the url to the file. This can be used to serve the file when needed. 
            fileurl = fs.url(file) 
       
            #form.save()
            item = Teacher()          
            item.birthday = request.POST['birthday']
            item.department_id = request.POST['department']
            item.picpath = fileurl
            item.user_id = user.pk
            #section.myclass_id = request.POST['myclass']
            item.save()
        else:        
            messages.error(request, request.POST['myclass'] )
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            #return HttpResponseRedirect('/thanks/')

        #return HttpResponse(user.pk)
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})
    # if a GET (or any other method) we'll create a blank form
    else: 
        form = TeacherForm()
        #formuser = UserForm()
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})

#
@login_required()
def add_notice(request):
    # if this is a POST request we need to process the form data
    config = Configurations.objects.filter(id = 1).first()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES) 
        # check whether it's valid:
        if form.is_valid(): 
            form.save()
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})
    # if a GET (or any other method) we'll create a blank form
    else: 
        form = TeacherForm()
        #formuser = UserForm()
        return render(request, 'configurations/add_event.html', {'form': form,  'config': config})

#
@login_required()
def add_event(request):
    # if this is a POST request we need to process the form data
    config = Configurations.objects.filter(id = 1).first()
    if request.method == 'POST':
        form = TeacherForm(request.POST, request.FILES) 
        # check whether it's valid:
        if form.is_valid(): 
            form.save()
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})
    # if a GET (or any other method) we'll create a blank form
    else: 
        form = TeacherForm()
        #formuser = UserForm()
        return render(request, 'configurations/add_student.html', {'form': form,  'config': config})
