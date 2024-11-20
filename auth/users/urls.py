from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import RegisterView, LoginView, UserView, LogoutView, AddStudentView, AddTeacherView, AddSchoolView, \
    SchoolView, LoginSchoolView, LogoutSchoolView, ClassView, AddClassView, EditClassView, DeleteClassView, \
    AddClassStudentView, ClassStudentView, DeleteClassStudentView, UserProfileView, UserProfileEditView, \
    SchoolProfileView, SchoolProfileEditView,StudentProfileView, StudentProfileEditView, TeacherProfileView, \
    TeacherProfileEditView

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
    path('user/profile/', UserProfileView.as_view()),
    path('user/profile_edit/', UserProfileEditView.as_view()),
    path('shcool/profile/', SchoolProfileView.as_view()),
    path('school/profile_edit/', SchoolProfileEditView.as_view()),
    path('student/profile/', StudentProfileView.as_view()),
    path('student/profile_edit/', StudentProfileEditView.as_view()),
    path('teacher/profile/', TeacherProfileView.as_view()),
    path('teacher/profile_edit/', TeacherProfileEditView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
