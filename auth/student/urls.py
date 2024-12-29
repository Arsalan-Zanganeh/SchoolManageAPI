from django.urls import path
from .views import StudentLoginView, StudentLogoutView, StudentView, StudentClassesView, ParentLogin, ParentLogoutView, \
    ParentClassesView, ParentEnterClass, ParentSeeHomeworkRecords, ParentCheckStudentAttendance, ParentShowQuizRecords, \
    DisciplinaryCaseList, DisciplineScore, RecentQuizTest, RecentHomework, RecentQuizExplan

urlpatterns = [
    path('login/', StudentLoginView.as_view()),
    path('logout/', StudentLogoutView.as_view()),
    path('user/', StudentView.as_view()),
    path('classes/', StudentClassesView.as_view()),
    path('parent-login/', ParentLogin.as_view()),
    path('parent-logout/', ParentLogoutView.as_view()),
    path('parent-classes/', ParentClassesView.as_view()),
    path('parent-enter-class/', ParentEnterClass.as_view()),
    path('parent-see-homeworks/', ParentSeeHomeworkRecords.as_view()),
    path('parent-attendance/', ParentCheckStudentAttendance.as_view()),
    path('parent-quiz-records/', ParentShowQuizRecords.as_view()),
    path('parent-disciplinary-cases/', DisciplinaryCaseList.as_view()),
    path('parent-discipline-score/', DisciplineScore.as_view()),
    path('recent-quiz-test/', RecentQuizTest.as_view()),
    path('recent-homework/', RecentHomework.as_view()),
    path('recent-quiz-explan/', RecentQuizExplan.as_view()),
]