from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, AddStudentView, AddTeacherView, AddSchoolView, \
    SchoolView, LoginSchoolView, LogoutSchoolView, ClassView, AddClassView, EditClassView, DeleteClassView, \
    AddClassStudentView, ClassStudentView, DeleteClassStudentView

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
    path('edit_class/', EditClassView.as_view()),
    path('delete_class/', DeleteClassView.as_view()),
    path('add_class_student/', AddClassStudentView.as_view()),
    path('class_student/', ClassStudentView.as_view()),
    path('delete_class_student/', DeleteClassStudentView.as_view()),
]