from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .views import RegisterView, LoginView, UserView, LogoutView, AddStudentView, AddTeacherView, AddSchoolView, \
    SchoolView, LoginSchoolView, LogoutSchoolView, ClassView, AddClassView, EditClassView, DeleteClassView, \
    AddClassStudentView, ClassStudentView, DeleteClassStudentView, UserProfileView, UserProfileEditView, \
    SchoolProfileView, SchoolProfileEditView, StudentProfileView, StudentProfileEditView, TeacherProfileView, \
    TeacherProfileEditView, NotificationSchoolView, NotificationAddView, NotificationStudentView, \
    NotificationUnseenCountStudentView, PasswordTokenCheckAPI, RequestPasswordResetEmailView, \
    SetNewPasswordAPIView, CreateNewQuizView, TeacherQuizesView, StartQuizView, StudentQuizView, \
    StudentRequestPasswordResetEmailView, StudentSetNewPasswordAPIView, StudentPasswordTokenCheckAPI, \
    TeacherRequestPasswordResetEmailView, TeacherSetNewPasswordAPIView, TeacherPasswordTokenCheckAPI, \
    QuizQuestionsTeacherView, AddQuizQuestionView, DeleteQuizQuestionView, EditQuizQuestionView, \
    StudentAnswerQuestion, StudentShowQuestions, StudentStartExam, TeacherWatchRecords, \
    StudentfinishExam, RecordToStudent, StudentShowRecords, StudentShowAnswers, HallandSubmitRecord, \
    HallandRecordsView, TeacherClassStudentView, TeacherEnterClass, StudentEnterClass, StudentSeeHomeworkRecords, \
    StudentSendHomework, StudentSeeHomeworks, TeacherAllHomeWorks, TeacherPublishHomeWork, TeacherDeleteHomeWork, \
    TeacherEditHomeWork, TeacherAddHomeWork

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('user/', UserView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('add_student/', AddStudentView.as_view()),
    path('add_teacher/', AddTeacherView.as_view()),
    path('add_school/', AddSchoolView.as_view()),
    path('school/', SchoolView.as_view()),
    path('login_school/', LoginSchoolView.as_view()),
    path('logout_school/', LogoutSchoolView.as_view()),
    path('classes/', ClassView.as_view()),
    path('add_class/', AddClassView.as_view()),
    path('edit_class/', EditClassView.as_view()),
    path('delete_class/', DeleteClassView.as_view()),
    path('add_class_student/', AddClassStudentView.as_view()),
    path('class_student/', ClassStudentView.as_view()),
    path('delete_class_student/', DeleteClassStudentView.as_view()),
    path('user/profile/', UserProfileView.as_view()),
    path('user/profile_edit/', UserProfileEditView.as_view()),
    path('school/profile/', SchoolProfileView.as_view()),
    path('school/profile_edit/', SchoolProfileEditView.as_view()),
    path('student/profile/', StudentProfileView.as_view()),
    path('student/profile_edit/', StudentProfileEditView.as_view()),
    path('teacher/profile/', TeacherProfileView.as_view()),
    path('teacher/profile_edit/', TeacherProfileEditView.as_view()),
    path('notify/', NotificationSchoolView.as_view()),
    path('add_notification/', NotificationAddView.as_view()),
    path('notifications/', NotificationStudentView.as_view()),
    path('unseen_notifications/', NotificationUnseenCountStudentView.as_view()),
    path('password-reset/<uibd64>/<token>/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('request-reset-email/',RequestPasswordResetEmailView.as_view(), name='request-reset-email'),
    path('password-reset-complete/', SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
    path('create_quiz/', CreateNewQuizView.as_view()),
    path('teacher_quizzes/', TeacherQuizesView.as_view()),
    path('start_quiz/',StartQuizView.as_view()),
    path('student_quizzes/', StudentQuizView.as_view()),
    path('student-reset-email/', StudentRequestPasswordResetEmailView.as_view()),
    path('student-reset-complete/', StudentSetNewPasswordAPIView.as_view()),
    path('student-password-reset/<uibd64>/<token>/', StudentPasswordTokenCheckAPI.as_view(),name='student-password-reset-confirm'),
    path('teacher-reset-email/', TeacherRequestPasswordResetEmailView.as_view()),
    path('teacher-reset-complete/', TeacherSetNewPasswordAPIView.as_view()),
    path('teacher-password-reset/<uibd64>/<token>/', TeacherPasswordTokenCheckAPI.as_view(),name='teacher-password-reset-confirm'),
    path('teacher-quiz-questions/', QuizQuestionsTeacherView.as_view()),
    path('teacher-add-quiz-question/', AddQuizQuestionView.as_view()),
    path('teacher-edit-quiz-question/', EditQuizQuestionView.as_view()),
    path('teacher-delete-quiz-question/', DeleteQuizQuestionView.as_view()),
    path('student-answer-question/', StudentAnswerQuestion.as_view()),
    path('student-show-questions/', StudentShowQuestions.as_view()),
    path('student-start-exam/', StudentStartExam.as_view()),
    path('student-finish-exam/', StudentfinishExam.as_view()),
    path('teacher-watch-records/', TeacherWatchRecords.as_view()),
    path('teacher-watch-record/', RecordToStudent.as_view()),
    path('student-show-records/', StudentShowRecords.as_view()),
    path('student-show-answers/', StudentShowAnswers.as_view()),
    path('student-submit-halland/', HallandSubmitRecord.as_view()),
    path('student-watch-halland-records/', HallandRecordsView.as_view()),
    path('teacher-class-students/', TeacherClassStudentView.as_view()),
    path('teacher-login-class/', TeacherEnterClass.as_view()),
    path('student-login-class/', StudentEnterClass.as_view()),
    path('student-homework-records/', StudentSeeHomeworkRecords.as_view()),
    path('student-send-homework/', StudentSendHomework.as_view()),
    path('student-see-homeworks/', StudentSeeHomeworks.as_view()),
    path('teacher-all-homeworks/', TeacherAllHomeWorks.as_view()),
    path('teacher-publish-homework/', TeacherPublishHomeWork.as_view()),
    path('teacher-delete-homework/', TeacherDeleteHomeWork.as_view()),
    path('teacher-edit-homework/', TeacherEditHomeWork.as_view()),
    path('teacher-add-homework/', TeacherAddHomeWork.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)