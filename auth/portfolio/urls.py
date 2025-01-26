from django.urls import path
from .views import StudentFiles, TeacherFiles, FilterStudents, StudentPictureTeacherSideView, \
    TeacherPicturePrincipalSideView, ChatInfoView

urlpatterns = [
    path('student_files/', StudentFiles.as_view()),
    path('teacher_files/', TeacherFiles.as_view()),
    path('filter_students/', FilterStudents.as_view()),
    path('StudentPicture_TeacherSideView/', StudentPictureTeacherSideView.as_view()),
    path('TeacherPicture_PrincipalSideView/', TeacherPicturePrincipalSideView.as_view()),
    path('chat_info/', ChatInfoView.as_view()),
]