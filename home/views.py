from exam.views import Exam_type
from django.http import HttpResponse
from django.shortcuts import render

from .forms import RegistrationForm
from django.http import HttpResponseRedirect 

from django.contrib.auth.decorators import login_required, permission_required
from configurations.models import Configurations, Student, Teacher, Class
from exam.models import Exam
from datetime import datetime, date, timedelta


# Create your views here.
def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'home/register.html', {'form': form})

#@login_required(redirect_field_name="/polls/3")
@login_required()
#@permission_required('home.index', raise_exception=True)
def index(request):
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
    return render(request, 'home/index.html',{
                                                'group':group ,
                                                'config':config,
                                                'totalStudents':totalStudents,
                                                'totalClasses':totalClasses,
                                                'totalTeachers':totalTeachers,
                                                'exams':exams,
                                                'Exam_types':Exam_type
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)