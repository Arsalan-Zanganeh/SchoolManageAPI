from django.urls import path
from .views import StudentLoginView, StudentLogoutView, StudentView

urlpatterns = [
    path('login/', StudentLoginView.as_view()),
    path('logout/', StudentLogoutView.as_view()),
    path('user/', StudentView.as_view()),
]