from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, AddStudentView, AddTeacherView, AddSchoolView, \
    SchoolView, LoginSchoolView, LogoutSchoolView, ClassView, AddClassView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('add_student/', AddStudentView.as_view()),
    path('add_teacher/', AddTeacherView.as_view()),
    path('add_school/', AddSchoolView.as_view()),
    path('school/', SchoolView.as_view()),
    path('login_school/', LoginSchoolView.as_view()),
    path('logout_school/', LogoutSchoolView.as_view()),
    path('classes/', ClassView.as_view()),
    path('add_class/', AddClassView.as_view()),
]