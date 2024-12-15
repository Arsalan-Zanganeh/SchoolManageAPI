from django.urls import path
from .views import DisciplineScoreChange, DisciplineScoreList, DisciplinaryCaseList, DisciplinaryCaseAdd, \
    DisciplinaryCaseDelete, StudentsofSchool, TeacherWatchStudentHomeworkAnswers, \
    TeacherAddChangeHomeworkGrade, TeacherAddFileEducationalContent, TeacherDeleteFileEducationalContent, \
    TeacherWatchFileEducationalContent, TeacherAddVideoEducationalContent, TeacherDeleteVideoEducationalContent, \
    TeacherWatchVideoEducationalContent, StudentWatchVideoEducationalContent, StudentWatchFileEducationalContent

urlpatterns = [
    path('score-list/', DisciplineScoreList.as_view()),
    path('score-change/', DisciplineScoreChange.as_view()),
    path('case-list/', DisciplinaryCaseList.as_view()),
    path('case-add/', DisciplinaryCaseAdd.as_view()),
    path('case-delete/', DisciplinaryCaseDelete.as_view()),
    path('school-students/', StudentsofSchool.as_view()),
    path('teacher-watch-homework-answers/', TeacherWatchStudentHomeworkAnswers.as_view()),
    path('teacher-addorchange-homework-grade/', TeacherAddChangeHomeworkGrade.as_view()),
    path('teacher-addfile-EC/', TeacherAddFileEducationalContent.as_view()),
    path('teacher-delfile-EC/', TeacherDeleteFileEducationalContent.as_view()),
    path('teacher-watchfile-EC/', TeacherWatchFileEducationalContent.as_view()),
    path('teacher-addvid-EC/', TeacherAddVideoEducationalContent.as_view()),
    path('teacher-delvid-EC/', TeacherDeleteVideoEducationalContent.as_view()),
    path('teacher-watchvid-EC/', TeacherWatchVideoEducationalContent.as_view()),
    path('student-watchvid-EC/', StudentWatchVideoEducationalContent.as_view()),
    path('student-watchfile-EC/', StudentWatchFileEducationalContent.as_view()),
]