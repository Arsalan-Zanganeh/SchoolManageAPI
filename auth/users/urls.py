from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import RegisterView, LoginView, UserView, LogoutView, AddStudentView, AddTeacherView, AddSchoolView, \
    SchoolView, LoginSchoolView, LogoutSchoolView, ClassView, AddClassView, EditClassView, DeleteClassView, \
    AddClassStudentView, ClassStudentView, DeleteClassStudentView, UserProfileView, UserProfileEditView, \
    SchoolProfileView, SchoolProfileEditView,StudentProfileView, StudentProfileEditView, TeacherProfileView, \
    TeacherProfileEditView, NotificationSchoolView, NotificationAddView, NotificationStudentView, \
    NotificationUnseenCountStudentView, PasswordTokenCheckAPI, RequestPasswordResetEmailView, \
    SetNewPasswordAPIView

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
    path('school/profile/', SchoolProfileView.as_view()),
    path('school/profile_edit/', SchoolProfileEditView.as_view()),
    path('student/profile/', StudentProfileView.as_view()),
    path('student/profile_edit/', StudentProfileEditView.as_view()),
    path('teacher/profile/', TeacherProfileView.as_view()),
    path('teacher/profile_edit/', TeacherProfileEditView.as_view()),
    path('notify/', NotificationSchoolView.as_view()),
    path('add_notification/', NotificationAddView.as_view()),
    path('notifications/', NotificationStudentView.as_view()),
    path('unseen_notifications/', NotificationUnseenCountStudentView.as_view()),
    # path('reset_password/' , auth_views.PasswordResetView.as_view(), name='reset_password'),
    # path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password-reset/<uibd64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('request-reset-email/',RequestPasswordResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
