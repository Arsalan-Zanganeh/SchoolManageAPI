from django.urls import path
from .views import DisciplineScoreChange, DisciplineScoreList, DisciplinaryCaseList, DisciplinaryCaseAdd, \
    DisciplinaryCaseDelete, StudentsofSchool, TeacherWatchStudentHomeworkAnswers, \
    TeacherAddChangeHomeworkGrade

urlpatterns = [
    path('score-list/', DisciplineScoreList.as_view()),
    path('score-change/', DisciplineScoreChange.as_view()),
    path('case-list/', DisciplinaryCaseList.as_view()),
    path('case-add/', DisciplinaryCaseAdd.as_view()),
    path('case-delete/', DisciplinaryCaseDelete.as_view()),
    path('school-students/', StudentsofSchool.as_view()),
    path('teacher-watch-homework-answers/', TeacherWatchStudentHomeworkAnswers.as_view()),
    path('teacher-addorchange-homework-grade/', TeacherAddChangeHomeworkGrade.as_view()),
]