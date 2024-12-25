from django.urls import path
from .views import DisciplineScoreChange, DisciplineScoreList, DisciplinaryCaseList, DisciplinaryCaseAdd, \
    DisciplinaryCaseDelete, StudentsofSchool, TeacherWatchStudentHomeworkAnswers, \
    TeacherAddChangeHomeworkGrade, TeacherAddFileEducationalContent, TeacherDeleteFileEducationalContent, \
    TeacherWatchFileEducationalContent, TeacherAddVideoEducationalContent, TeacherDeleteVideoEducationalContent, \
    TeacherWatchVideoEducationalContent, StudentWatchVideoEducationalContent, StudentWatchFileEducationalContent, \
    StudentAddPlan, StudentWatchPlans, StudentDeletePlan, TeacherWatchStudentPlans, TeacherAddFeedback, \
    TeacherDeleteFeedback, TeacherWatchFeedbacks, WSGetID, TeacherAddStudentPlan, TeacherDeletePlan

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
    path('student-add-plan/', StudentAddPlan.as_view()),
    path('teacher-add-student-plan/', TeacherAddStudentPlan.as_view()),
    path('student-watch-plans/', StudentWatchPlans.as_view()),
    path('student-delete-plan/', StudentDeletePlan.as_view()),
    path('teacher-delete-plan/', TeacherDeletePlan.as_view()),
    path('teacher-watch-student-plans/', TeacherWatchStudentPlans.as_view()),
    path('teacher-add-feed-back/', TeacherAddFeedback.as_view()),
    path('teacher-delete-feedback/', TeacherDeleteFeedback.as_view()),
    path('teacher-watch-feedbacks/', TeacherWatchFeedbacks.as_view()),
    path('WS-getid/', WSGetID.as_view()),
]