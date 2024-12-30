from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import NotificationSchoolView, NotificationAddView, NotificationStudentView, \
    NotificationUnseenCountStudentView, NotificationStudentSingleSeen

urlpatterns = [
    path('notify/', NotificationSchoolView.as_view()),
    path('add_notification/', NotificationAddView.as_view()),
    path('notifications/', NotificationStudentView.as_view()),
    path('unseen_notifications/', NotificationUnseenCountStudentView.as_view()),
    path('student-single-notif-seen/', NotificationStudentSingleSeen.as_view()),
]