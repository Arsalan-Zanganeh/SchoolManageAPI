from django.contrib import admin

# Register your models here.
from .models import User, School, Student, Teacher, Classes, ClassStudent, UserProfile

admin.site.register(User)
admin.site.register(School)
admin.site.register(Student)
admin.site.register(Teacher)
admin.site.register(Classes)
admin.site.register(ClassStudent)
admin.site.register(UserProfile)