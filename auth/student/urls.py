from django.urls import path
from .views import StudentLoginView, StudentLogoutView, StudentView, StudentClassesView

urlpatterns = [
    path('login/', StudentLoginView.as_view()),
    path('logout/', StudentLogoutView.as_view()),
    path('user/', StudentView.as_view()),
    path('classes/', StudentClassesView.as_view()),
]