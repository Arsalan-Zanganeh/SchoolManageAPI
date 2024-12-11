from django.urls import path
from .views import TeacherView, TeacherLogoutView, TeacherLoginView, TeacherClassesView, TeacherClassStudentsView, \
    TeacherWatchAttendance, TeacherCheckStudentAttendance

urlpatterns = [
    path('login/', TeacherLoginView.as_view()),
    path('logout/', TeacherLogoutView.as_view()),
    path('user/', TeacherView.as_view()),
    path('classes/', TeacherClassesView.as_view()),
    path('class-students/', TeacherClassStudentsView.as_view()),
    path('watch-attendance/', TeacherWatchAttendance.as_view()),
    path('check-student-attendance/', TeacherCheckStudentAttendance.as_view()),
]