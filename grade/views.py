from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models import Avg
#
from configurations.models import Class, Configurations, Course, Section, Student, Teacher, Grade, CourseOfSection, GradeOfVN
from exam.views import Exam_type
from exam.models import Exam, Room, GradeOfExam
from .forms import SummaryForm
# thông báo lỗi
from django.contrib import messages 

# generate pdf Using WeasyPrint
from django.core.files.storage import FileSystemStorage
#from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML
from library.functions import rank_course, rank_mark
# Create your views here.
@login_required()
@permission_required('grade.courseOfTeacher', raise_exception=True)
def CourseOfTeacher(request, examcourse_id):
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

@login_required()
@permission_required('configurations.view_gradeofvn', raise_exception=True)
def print_marks_course(request, course_id):
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    
    courseOfSection = CourseOfSection.objects.filter(id = course_id).first()
    grades = GradeOfVN.objects.filter(courseOfSection_id = course_id)
    List_marks_course = []
    countRankXS =0
    countRankG = 0
    countRankKha = 0
    countRankTBK =0
    countRankTB =0
    countRankY =0
    if grades :

        for grade in grades:
          
            
                att = dict()
                
                att['codeStudent'] = grade.student
                att['nameStudent'] = grade.student.getname

                List_pointTX = []
                if(grade.coefficient_1_1>=0):
                    List_pointTX.append(grade.coefficient_1_1)
                if(grade.coefficient_1_2>=0):
                    List_pointTX.append(grade.coefficient_1_2)
                
                att['List_pointTX'] = List_pointTX
                att['widthTX'] = round(100/len(List_pointTX))

                List_pointDK = []
                if(grade.coefficient_2_1>=0):
                    List_pointDK.append(grade.coefficient_2_1)
                #if(grade.coefficient_2_2>=0):
                #    List_pointDK.append(grade.coefficient_2_2)
                
                att['List_pointDK'] = List_pointDK
                att['widthDK'] = round(100/len(List_pointDK))

                end_mark = grade.end_mark_1_1
                att['end_mark'] = end_mark

                total_mark_course = grade.total_mark_course
                att['total_mark_course'] = total_mark_course
                rank_mark = rank_course(end_mark, total_mark_course,countRankXS,countRankG,countRankKha,countRankTBK,countRankTB,countRankY)
                #return HttpResponse(rank_mark)
                att['rank_course'] = rank_mark['rank']
                countRankXS = rank_mark['countRankXS']
                countRankG = rank_mark['countRankG']
                countRankKha = rank_mark['countRankKha'] 
                countRankTBK =rank_mark['countRankTBK'] 
                countRankTB =rank_mark['countRankTB'] 
                countRankY =rank_mark['countRankY'] 
                List_marks_course.append(att)

    List_rank_course = []
    countRank =grades.count()
   
    list_rank = dict()  
    list_rank['rank'] = "Xuất sắc"
    list_rank['countRank'] = countRankXS
    list_rank['percentRank'] = round( int(countRankXS)*100/countRank,2)
    if countRankXS>0:
        List_rank_course.append(list_rank)

    list_rank = dict()  
    list_rank['rank'] = "Giỏi"
    list_rank['countRank'] = countRankG
    list_rank['percentRank'] = round( int(countRankG)*100/countRank,2)
    if countRankG>0:
        List_rank_course.append(list_rank)
    
    list_rank = dict()  
    list_rank['rank'] = "Khá"
    list_rank['countRank'] = countRankKha
    list_rank['percentRank'] = round( int(countRankKha)*100/countRank,2)
    if countRankKha>0:
        List_rank_course.append(list_rank)
    
    list_rank = dict()  
    list_rank['rank'] = "TBK"
    list_rank['countRank'] = countRankTBK
    list_rank['percentRank'] = round( int(countRankTBK)*100/countRank,2)
    if countRankTBK>0:
        List_rank_course.append(list_rank)
    
    list_rank = dict()  
    list_rank['rank'] = "TB"
    list_rank['countRank'] = countRankTB
    list_rank['percentRank'] = round( int(countRankTB)*100/countRank,2)
    if countRankTB>0:
        List_rank_course.append(list_rank)
     
    list_rank = dict()  
    list_rank['rank'] = "Yếu"
    list_rank['countRank'] = countRankY
    list_rank['percentRank'] = round( int(countRankY)*100/countRank,2)
    if countRankY>0:
        List_rank_course.append(list_rank)

    html_string = render_to_string('pdf_diemtkmonhoc.html', {'paragraphs': paragraphs,
                                                            'department':'KHOA KHCB',
                                                            'course': courseOfSection,
                                                            'class': 'Y49A',
                                                            'List_rank_course': List_rank_course,
                                                             'List_marks_course':List_marks_course,
                                                            })
    
    html = HTML(string=html_string)
    html.write_pdf(target='media/pdf_diemtkmonhoc.pdf')   

    fs = FileSystemStorage()
    with fs.open('pdf_diemtkmonhoc.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_diemtkmonhoc.pdf"'
        return response
    
    
    return None

@login_required()
@permission_required('grade.history', raise_exception=True)
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

#-------------------------------------------------------------
def myKeySort(e):
  return e['average_total_mark_course']
  

@login_required()
@permission_required('grade.summary', raise_exception=True)
def summary(request):
    config = Configurations.objects.filter(id = 1).first()
    form = SummaryForm()
    #return HttpResponse(request.POST)
    if request.method == 'POST':
        if 'myClass' in request.POST:
            myClass = request.POST['myClass']
            #return HttpResponse(myClass)
            students= Student.objects.filter(myclass_id=myClass)
        if 'textsection' in request.POST:
            textsection = request.POST['textsection']
            textsection = textsection.split(",")
            #return HttpResponse(myClass)
            courseOfSection = []
            for section_id in textsection:    
                course = CourseOfSection.objects.filter(section_id = section_id)
                courseOfSection.append(course)

            total_mark= []
            for student in students:
                temp_grade =0
                imark = 0
                list_grades = []
                is_total_mark_course = True
                for section_id in textsection:
                        
                    #courseOfSection = CourseOfSection.objects.filter(section_id = section_id)
                    
                    #grade = GradeOfVN.objects.filter(courseOfSection__section_id = section_id,
                    #    student_id = student.id).aggregate(average_total_mark_course=Avg('total_mark_course'))
                    #temp_grade = temp_grade + grade['average_total_mark_course']
                   
                    grades = GradeOfVN.objects.filter(courseOfSection__section_id = section_id,
                        student_id = student.id)
                    for grade in grades:
                        
                        #return HttpResponse(grade.total_mark_course)
                        #// nếu điểm < 5 thì không tổng kết
                        t_grade = grade.total_mark_course
                        if t_grade>=5:
                            imark = imark + 1
                            temp_grade = temp_grade + t_grade
                            list_grades.append(grade)
                        else:
                            imark = imark + 1
                            temp_grade = temp_grade + t_grade
                            list_grades.append(grade)
                            is_total_mark_course = False
                            #break
                

                #return HttpResponse(list_grades)
                total_mark_course = dict()  
                total_mark_course['student'] = student
                total_mark_course['list_grades'] = list_grades
                _markTB = round(temp_grade/imark, 2)
                total_mark_course['average_total_mark_course'] = _markTB
                total_mark_course['rank'] = rank_mark(_markTB)
                
                total_mark_course['is_total_mark_course'] = is_total_mark_course
                total_mark.append(total_mark_course)
                #return HttpResponse(total_mark)
            #return render(request, 'grade/total-mark.html',{'form': form,  'config': config} )
                total_mark.sort(reverse=True, key=myKeySort)
        paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
        html_string = render_to_string('pdf_summary.html', {'paragraphs': paragraphs,
                                                                'department':'KHOA KHCB',
                                                                'total_mark': total_mark,
                                                                'courseOfSection':courseOfSection,
                                                                'class': 'Y49A',                                                          
                                                            })
        
        html = HTML(string=html_string)
        html.write_pdf(target='media/pdf_summary.pdf')   

        fs = FileSystemStorage()
        with fs.open('pdf_summary.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="pdf_summary.pdf"'
            return response
        
        
        return None
        
    #---------------------------------------------
    return render(request, 'grade/summary.html',{'form': form,  'config': config} )
    




