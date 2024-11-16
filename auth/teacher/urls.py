from django.urls import path
from .views import TeacherView, TeacherLogoutView, TeacherLoginView, TeacherClassesView

urlpatterns = [
    path('login/', TeacherLoginView.as_view()),
    path('logout/', TeacherLogoutView.as_view()),
    path('user/', TeacherView.as_view()),
    path('classes/', TeacherClassesView.as_view()),
]