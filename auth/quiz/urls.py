from django.urls import path
from .views import CreateNewQuizView, TeacherQuizesView, StartQuizView, StudentQuizView, \
    QuizQuestionsTeacherView, AddQuizQuestionView, DeleteQuizQuestionView, EditQuizQuestionView, \
    StudentAnswerQuestion, StudentShowQuestions, TeacherWatchRecords, \
    StudentfinishExam, RecordToStudent, StudentShowRecord,StudentExtraFinish, \
    QuizQuestionStudentView, QuizFinishedBoolean

urlpatterns = [
    path('create_quiz/', CreateNewQuizView.as_view()),
    path('teacher_quizzes/', TeacherQuizesView.as_view()),
    path('start_quiz/',StartQuizView.as_view()),
    path('student_quizzes/', StudentQuizView.as_view()),
    path('teacher-quiz-questions/', QuizQuestionsTeacherView.as_view()),
    path('teacher-add-quiz-question/', AddQuizQuestionView.as_view()),
    path('teacher-edit-quiz-question/', EditQuizQuestionView.as_view()),
    path('teacher-delete-quiz-question/', DeleteQuizQuestionView.as_view()),
    path('student-answer-question/', StudentAnswerQuestion.as_view()),
    path('student-show-questions/', StudentShowQuestions.as_view()),
    path('student-finish-exam/', StudentfinishExam.as_view()),
    path('teacher-watch-records/', TeacherWatchRecords.as_view()),
    path('teacher-watch-record/', RecordToStudent.as_view()),
    path('student-show-record/', StudentShowRecord.as_view()),
    path('student-extra-finish/', StudentExtraFinish.as_view()),
    path('student-quiz-prev-answers/', QuizQuestionStudentView.as_view()),
    path('student-quiz-finished-boolean/', QuizFinishedBoolean.as_view()),
]