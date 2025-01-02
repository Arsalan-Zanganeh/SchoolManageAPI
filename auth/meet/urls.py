from django.urls import path
from .views import TeacherEnterOnlineClass, StudentEnterOnlineClass

urlpatterns = [
    path('teacher-enter/', TeacherEnterOnlineClass.as_view()),
    path('student-enter/', StudentEnterOnlineClass.as_view()),
]