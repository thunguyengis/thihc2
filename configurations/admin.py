from django.contrib import admin

#from .models import Setting
# Register your models here.
from .models import Configurations, Employee, Department, Teacher, Majors, Class, Student, Section, Course
from .models import CoursOfDepartment, CourseOfSection

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User


# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
class EmployeeInline(admin.StackedInline):
    model = Employee
    can_delete = False
    verbose_name_plural = 'employee'

# Define a new User admin
class UserAdmin1(BaseUserAdmin):
    
    inlines = (EmployeeInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin1)

admin.site.register(Configurations)


admin.site.register(Department)
admin.site.register(Teacher)

admin.site.register(Majors)
admin.site.register(Class)
admin.site.register(Student)

admin.site.register(Section)
admin.site.register(Course)

admin.site.register(CoursOfDepartment)
admin.site.register(CourseOfSection)