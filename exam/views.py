from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from django.http import HttpResponseRedirect 
#
from django.contrib.auth.decorators import login_required, permission_required
#
from .models import Exam, Room, GradeOfExam
from .forms import ExamForm, RoomForm
#
from question.models import Answer, Question, QuestionOfExam
#
from configurations.models import Configurations, Course, Class, CourseOfSection, GradeOfVN, Section, Student
# để phân trang
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# generate CSV. 
from django.template import loader

# generate pdf
import io
from django.http import FileResponse
import time

# generate pdf Using WeasyPrint
from django.core.files.storage import FileSystemStorage
#from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

#
from django.db.models import Max
import random


# thông báo lỗi
from django.contrib import messages 
# Create your views here.

# Danh sách 
Exam_type = [
        ('coefficient_1_1', 'Hệ Số 1 Lần 1'),
        ('coefficient_1_2', 'Hệ Số 1 Lần 2'),
        ('coefficient_2_1', 'Hệ Số 2 Lần 1'),
        ('coefficient_2_2', 'Hệ Số 2 Lần 2 '),
        ('end_mark_1_1', 'Thi kết thúc môm '),
        ('coefficient_v2_1_1', 'Hệ Số 1 Lần 1 Thi lại'),
        ('coefficient_v2_1_2', 'Hệ Số 1 Lần 2 Thi lại'), 
        ('coefficient_v2_2_1', 'Hệ Số 2 Lần 1 Thi lại'),
        ('coefficient_v2_2_2', 'Hệ Số 2 Lần 2 Thi lại'),
        ('end_mark_v2_1_1', 'Thi kết thúc môm Thi lại'),
        ('practical_1_1', 'Thi Thực hành'),
        ('practical_v2_1_1', 'Thi Thực hành'),
    ]
@login_required()
@permission_required('exam.index', raise_exception=True)
def index(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
    config = Configurations.objects.filter(id = 1).first()
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(config)
    rooms = Room.objects.all()

    # loc các bài kiểm tra trong 1 tuần
   
    #Sample.objects.filter(date__range=[startdate, enddate])
    exams = Exam.objects.all()
    #lưu dữ liệu 
    #return HttpResponse("exam")
    if request.method == 'POST':
        #return HttpResponse("exam")
        id = request.POST['id']
        exam = Exam.objects.filter(id = id).first()
        
        if 'active' in request.POST and request.POST['active'] == 'on':
            exam.active = 1 #request.POST['active']
        if 'notice_published' in request.POST and request.POST['notice_published'] == 'on':
            exam.notice_published = 1 
        if 'result_published' in request.POST and request.POST['result_published'] == 'on':
            exam.result_published = 1
        
        exam.save() 
      
        gradeOfExams = GradeOfExam.objects.filter(exam_id = id)
        #return HttpResponse(gradeOfExams.count())
        
        key = 0
        for room in rooms:
           
            _i= str(room.id)
            
            if 'totalRoom'+_i in request.POST:
               
                totalRoom = int( request.POST['totalRoom'+ _i ] )
                #return HttpResponse(totalRoom)
               
                for i in range(totalRoom):
                   
                    gradeOfExam = gradeOfExams[key]
                    gradeOfExam.room_id = room.id
                    gradeOfExam.save()
                    key = key + 1
  
    # Phần exams
    page = request.GET.get('page', 1)

    paginator = Paginator(exams, 20)
    try:
        exams_page = paginator.page(page)
    except PageNotAnInteger:
        exams_page = paginator.page(1)
    except EmptyPage:
        exams_page = paginator.page(paginator.num_pages)
    #return HttpResponse(Exam_type[0][0])
    # DANH SÁCH PHONG THI, CAI ĐẶT SỐ THÍ SINH
   
    attCount = []    
    attStudent = []    
    if  exams :          
        for i, exam in enumerate(exams) :
           
            atS = dict()
            atS['exam_id'] = exam.id
            atS['totalStudent'] =  GradeOfExam.objects.filter(exam_id = exam.id).count()
            attStudent.append(atS)
            for k, room in enumerate(rooms) :
                at = dict()
                at['exam_id'] = exam.id
                at['room_id'] = room.id
                at['totalRoom'] = GradeOfExam.objects.filter(exam_id = exam.id).filter(room_id = room.id).count()
                attCount.append(at)
    #sreturn HttpResponse(attStudent)
    # danh sách câu hỏi
    #questions = Question.objects.all
    return render(request, 'exam/index.html',{
                                                'group':group ,
                                                'config':config,
                                                'exams':exams_page,
                                                'Exam_type':Exam_type,
                                                'rooms':rooms,
                                                'attCount':attCount,
                                                'attStudent':attStudent
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)
#################################################################################################
@login_required()

def thu(request):
    #myClass_id = request.GET.get('myClass',1)
    sections = Section.objects.filter(myclass_id=1)
    return render(request, 'exam/section_dropdown_list_options.html', {'sections': sections})
   
@login_required()
@permission_required('exam.ajax_load_sections', raise_exception=True)
def load_sections(request):
    myClass_id = request.GET.get('myClass')
    sections = Section.objects.filter(myclass_id=myClass_id)
    return render(request, 'exam/section_dropdown_list_options.html', {'sections': sections})
@login_required()
@permission_required('exam.ajax_load_courses', raise_exception=True)
def load_courses(request):
    section_id = request.GET.get('section')
    courses = CourseOfSection.objects.filter(section_id=section_id)
    return render(request, 'exam/course_dropdown_list_options.html', {'courses': courses})

@login_required()
@permission_required('exam.create', raise_exception=True)
def create(request):
    config = Configurations.objects.filter(id = 1).first()
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
    if request.method == 'POST':
        #form = ExamForm(request.POST) 
        # check whether it's valid:
        #myclass_id = request.POST['myclass']
        
        exam = Exam()
        if 'exam_name' in request.POST:
            exam.exam_name = request.POST['exam_name']
        if 'exam_type2' in request.POST:
            exam.exam_type2 = request.POST['exam_type2']
        if 'exam_code' in request.POST:
            exam.exam_code = request.POST['exam_code']
        if 'courseOfSection' in request.POST:
            exam.courseOfSection_id = request.POST['courseOfSection']
        if 'myClass' in request.POST:
            exam.myclass_id = request.POST['myClass']
            
        if 'active' in request.POST:
            exam.active = True
        if 'notice_published' in request.POST:
            exam.notice_published = request.POST['notice_published']
        if 'result_published' in request.POST:
            exam.result_published = request.POST['result_published']
        if 'time_exam' in request.POST:
            exam.time_exam = request.POST['time_exam']
        if 'start_date' in request.POST:
            exam.start_date = request.POST['start_date']
        if 'term' in request.POST:
            exam.term = request.POST['term']
            # exam.exam_name = form.cleaned_data['exam_name']term
        #exam.save()
        
        try:
            exam.save()
            #gradeOfVNs = GradeOfVN.objects.filter(courseOfSection_id = exam.courseOfSection_id )
            students =  Student.objects.filter(myclass_id = exam.myclass_id)
            #return HttpResponse(students)
            #for grade in gradeOfVNs :
                #addGradeOfExam(exam.id, grade.teacher_id, grade.student_id, request.user.id )
            for student in students :
                addGradeOfExam(exam.id, 1, student.id, request.user.id )
            #return render(request,S 'exam/index.html',{'group':group , 'config':config, })
            return redirect('/exam')
        except:
            #response = HttpResponse('<script>alert(\'You must remove an item before adding another\');</script>')
            #return response
            #url = '/exam/create'
            #resp_body = '<script>alert("You must remove an item before adding another");\
             #           window.location="%s"</script>' % url
            # return HttpResponse(resp_body)
            #return render(request, 'exam/index.html',{'group':group , 'config':config, })
            messages.error(request, "Thêm bài kiểm tra không thành công!!!")
            return render(request, 'exam/create.html', {  'config': config})

     
    # if a GET (or any other method) we'll create a blank form
    else: 
        form = ExamForm()
        #return HttpResponse(form)
        #formuser = UserForm()
        return render(request, 'exam/create.html', {'form': form,  'config': config})


# hàm đẻ thêm grade sau khi thêm course
def addGradeOfExam(exam_id, teacher_id, student_id , user_id):
    grade = GradeOfExam()
    grade.exam_id = exam_id
    grade.student_id = student_id
    grade.room_id = 1
    grade.user_id = user_id    
    grade.save()
    #return HttpResponse(exam_id)

@login_required()
@permission_required('exam.active', raise_exception=True)
def active(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
   
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    config = Configurations.objects.filter(id = 1).first()
    exams = Exam.objects.all()
    courses = CourseOfSection.objects.all()
    myclass = Class.objects.all()
   
    return render(request, 'exam/active.html',{
                                                'group':group ,
                                                'config':config,
                                                'exams':exams,
                                                'courses':courses,
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)

"""
Danh sách Phòng thi
"""
@login_required()
@permission_required('exam.room', raise_exception=True)
def room(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
    config = Configurations.objects.filter(id = 1).first()
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
   
    rooms = Room.objects.all()
    form = RoomForm()
   
    
   
    return render(request, 'exam/room.html',{
                                                'group':group ,
                                                'config':config,
                                                'rooms':rooms,
                                                 'form':form
                                                
                                             })
 
    #return HttpResponse(request.user.employee.picpath)
    #return HttpResponse(request.user.groups)

@login_required()
@permission_required('exam.add_room', raise_exception=True)
def add_room(request):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
                                      # QuerySet to `list`
    config = Configurations.objects.filter(id = 1).first()
    #for g in request.user.groups.all():
    #    l.append(g.name)
    #return HttpResponse(l)
    if request.method == 'POST':
        #form = ExamForm(request.POST, request.FILES) 
        # check whether it's valid:
        #form.myclass_id = request.POST['myclass']
        room = Room()
        if 'room_name' in request.POST:
            room.room_name = request.POST['room_name']
        if 'room_number_test' in request.POST:
            room.room_number_test = request.POST['room_number_test']
        room.save()

    return HttpResponseRedirect("/exam/room/")
    
@login_required()
def detail_roomCSV(request):
   # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="somefilename.csv"'

    # The data is hard-coded here, but you could load it from a database or
    # some other source.
    csv_data = (
        ('First row', 'Nguyên Thị Thu', 'Bar', 'Baz'),
        ('Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"),
    )

    t = loader.get_template('my_template_name.txt')
    c = {'data': csv_data}
    response.write(t.render(c))
    return response

@login_required()
def detail_roomPDF(request):
    '''canvas1 = canvas.Canvas('myfile.pdf', pagesize=A4)
    width, height = A4  
    canvas1.drawString(100,750,"Welcome to Reportlab!")
    canvas1.save()'''
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer,pagesize=A4)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.setLineWidth(.3)
    p.setFont('Helvetica', 12)
    p.drawString(30,750,'OFFICIAL COMMUNIQUE')
    p.drawString(30,735,'OF ACME INDUSTRIES')
    p.drawString(500,750,"12/12/2010")
    p.line(480,747,580,747)
    p.drawString(275,725,'AMOUNT OWED:')
    p.drawString(500,725,"$1,000.00")
    p.line(378,723,580,723)
    p.drawString(30,703,'RECEIVED BY:')
    p.line(120,700,580,700)
    p.drawString(120,703,"JOHN DOE")

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')
@login_required()
@permission_required('exam.detail_room', raise_exception=True)
def detail_room(request, exam_id):
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    rooms = Room.objects.all()
    List_Student_Room = []
    if rooms :
        for room in rooms:
            gradeOfExams = GradeOfExam.objects.filter(exam_id = exam_id, room_id = room.id)
            exam = Exam.objects.filter(id = exam_id).first()
            if gradeOfExams :
                att = dict()
                att['course'] = exam.courseOfSection
                att['class'] = exam.courseOfSection.getclass
                att['room_name'] = room.room_name
                att['gradeOfExams'] = gradeOfExams
                List_Student_Room.append(att)

             
           
    html_string = render_to_string('pdf_room.html', {'paragraphs': paragraphs,
                                                            'department':'KHOA KHCB',
                                                           
                                                            'class': 'Y49A',
                                                            'List_Student_Room':List_Student_Room,
                                                            })
    
    html = HTML(string=html_string)
    html.write_pdf(target='media/pdf_room.pdf')   

    fs = FileSystemStorage()
    with fs.open('pdf_room.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="pdf_room.pdf"'
        return response
    
    
    return None

def download_detail_room(file_name):
    fs = FileSystemStorage()
    with fs.open(file_name) as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response

#======================================
@login_required()
@permission_required('exam.detail_question', raise_exception=True)
def detail_question(request, exam_id):
    paragraphs = ['first paragraph', 'second paragraph', 'third paragraph']
    rooms = Room.objects.all()
    List_Student_Room = []
    if rooms :
        for room in rooms:
            gradeOfExams = GradeOfExam.objects.filter(exam_id = exam_id, room_id = room.id)
            exam = Exam.objects.filter(id = exam_id).first()
            if gradeOfExams :
                att = dict()
                att['course'] = exam.courseOfSection
                att['class'] = exam.courseOfSection.getclass
                att['room_name'] = room.room_name
                att['gradeOfExams'] = gradeOfExams
                List_Student_Room.append(att)

               
               
           
    html_string = render_to_string('pdf_template.html', {'paragraphs': paragraphs,
                                                            'department':'KHOA KHCB',
                                                           
                                                            'class': 'Y49A',
                                                            'List_Student_Room':List_Student_Room,
                                                            })
    html = HTML(string=html_string)     
    html.write_pdf(target='media/mypdf.pdf')   

    fs = FileSystemStorage()
    with fs.open('mypdf.pdf') as pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="mypdf.pdf"'
        return response
    
    
    return None

@login_required()
@permission_required('exam.setting_question', raise_exception=True)
def setting_question(request, exam_id):
    group = request.user.groups.values_list('name',flat = True).first() # QuerySet Object
    config = Configurations.objects.filter(id = 1).first()
    exam = Exam.objects.filter(id = exam_id).first()
    #question = Question.objects.filter(id = exam.courseOfSection.coursOfDepartment ).first()
    List_Chater_Question = []
    course_id = exam.courseOfSection.coursOfDepartment
    #if rooms :
    if request.method == 'POST':
        chapters  = None
        if 'chapter[]' in request.POST :
            chapters = request.POST.getlist("chapter[]")
        
        #return HttpResponse(request.POST)
        
        if chapters:
            QuestionOfExam.objects.filter(exam_id = exam_id).delete()
            for i, chapter in enumerate(chapters):
                
                j = i + 1
                if 'cb' + str(j) in request.POST:
                    intcb = int ( request.POST["cb" + str(j) ] )
                    question = Question.objects.filter(coursOfDepartment_id = course_id, chapter = chapter, question_level = 'cb')
                    #max_id = Question.objects.filter(coursOfDepartment_id = course_id, chapter = chapter, question_level = 'cb').aggregate(max_id=Max("id"))['max_id']
                    for icb in range(intcb):
                        pk = random.randint(0, question.count() -1 )
                        
                        while QuestionOfExam.objects.filter(exam_id = exam.id, question_id = question[pk].id).count() != 0 :
                            pk = random.randint(0, question.count() -1 )
                            #print (pk)
                        qExam = QuestionOfExam()
                        qExam.question_id = question[pk].id
                        qExam.exam_id = exam.id
                        qExam.user_id = request.user.id
                        qExam.save()
                   
                    #item_q = Question.objects.filter(coursOfDepartment_id = course_id, chapter = chapter, question_level = 'cb').get(pk=pk)
                    #if item_q:
                strnc = 'nc' + str(j)
                if strnc in request.POST:
                    strnc = request.POST[strnc]
                    if strnc != "":
                        intnc =  int( strnc )
                        question = Question.objects.filter(coursOfDepartment_id = course_id, chapter = chapter, question_level = 'nc')
                        for inc in range(intnc):
                            pk = random.randint(0, question.count() -1 )
                            while QuestionOfExam.objects.filter(exam_id = exam.id, question_id = question[pk].id).count() != 0 :
                                pk = random.randint(0, question.count() -1  )
                                #print (pk)
                            qExam = QuestionOfExam()
                            qExam.question_id = question[pk].id
                            qExam.exam_id = exam.id 
                            qExam.user_id = request.user.id
                            qExam.save()
        
                
        #return HttpResponse(request.POST)

    
    for i in range(11):
        j= i + 1
        questioncb = Question.objects.filter(coursOfDepartment_id = course_id, chapter = j, question_level = 'cb').count()
       
        questionnc = Question.objects.filter(coursOfDepartment_id = course_id, chapter = j, question_level = 'nc').count()
        
            #exam = Exam.objects.filter(id = exam_id).first()
       
        att = dict()
        
        
        if questioncb :
            att['questioncb'] = questioncb
            # lọc bằng cách join 2 bảng
            questioncbsetting = QuestionOfExam.objects.filter( exam_id = exam.id, question__question_level = 'cb', question__chapter = j).count()
            
            if questioncbsetting :
                att['questioncbsetting'] = questioncbsetting
        if questionnc :
            #return HttpResponse(questionnc)
            att['questionnc'] = questionnc
            questionncsetting = QuestionOfExam.objects.filter( exam_id = exam.id, question__question_level = 'nc', question__chapter = j).count()
            
            if questionncsetting :
                att['questionncsetting'] = questionncsetting
        if att :
            att['chapter'] = j
            List_Chater_Question.append(att)
   
        #return HttpResponse(att)
    return render(request, 'exam/setting_question.html',{
                                                'group':group ,
                                                'config':config,
                                                'exam':exam,
                                                'List_Chater_Question':List_Chater_Question,
                                                #'rooms':rooms,
                                                #'form':form
                                                
                                             })

@login_required()
def generate_exam(request, exam_id):
    #Answer.objects.
    return
