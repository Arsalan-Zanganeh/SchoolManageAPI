from django.urls import path
from .views import DisciplineScoreChange, DisciplineScoreList, DisciplinaryCaseList, DisciplinaryCaseAdd, \
    DisciplinaryCaseDelete, StudentsofSchool

urlpatterns = [
    path('score-list/', DisciplineScoreList.as_view()),
    path('score-change/', DisciplineScoreChange.as_view()),
    path('case-list/', DisciplinaryCaseList.as_view()),
    path('case-add/', DisciplinaryCaseAdd.as_view()),
    path('case-delete/', DisciplinaryCaseDelete.as_view()),
    path('school-students/', StudentsofSchool.as_view()),
]