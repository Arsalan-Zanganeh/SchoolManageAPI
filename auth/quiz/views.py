from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime
from users.models import Teacher, Student, Classes, QuizTeacherExplan, QuizQuestionExplan, \
    QuizStudentRecordExplan, QuizQuestionStudentExplan

from users.serializers import CreateNewQuizExplanSerializer, AddQuizQuestionExplanSerializer, \
    TeacherQuizExplanSerializer, StudentQuizRecordExplanSerializer, QuizQuestionStudentExplanSerializer, \
    StudentSerializer, StudentQuestionExplanSerializer

class CreateNewQuizView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()

        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        myquiz = QuizTeacherExplan.objects.create(Title=request.data['Title'], Teacher=teacher, Classes=myclass,
                                   OpenTime=datetime.datetime.now() + datetime.timedelta(days=1),
                                   DurationHour=0, DurationMinute=0)
        myquiz.save()
        serializer = CreateNewQuizExplanSerializer(myquiz)
        return Response(serializer.data)

class AddQuizQuestionView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacherExplan.objects.filter(Teacher=teacher, id=request.data['QuizTeacherExplan']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("You can not change this quiz")
        question = QuizQuestionExplan.objects.create(QuizTeacherExplan=quiz, Question=request.data['Question'],
                                                     Zarib=request.data['Zarib'], Answer=request.data['Answer'])
        question.save()
        return Response({'message':'Your question has been added'})

class DeleteQuizQuestionView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacherExplan.objects.filter(Teacher=teacher, id=request.data['QuizTeacherExplan']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("You can not change this quiz")
        question = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quiz, pk=request.data['Question_ID']).first()
        question.delete()
        return Response({'message':'Your question has been deleted'})

class EditQuizQuestionView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacherExplan.objects.filter(Teacher=teacher, id=request.data['QuizTeacherExplan']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("You can not change this quiz")
        question = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quiz, pk=request.data['Question_ID']).first()
        question.Question = request.data['Question']
        question.Zarib=request.data['Zarib']
        question.save()
        return Response({'message':'Your question has been edited'})

class QuizQuestionsTeacherView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        quiz = QuizTeacherExplan.objects.filter(Teacher=teacher, id=request.data['QuizTeacherExplan']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        questions = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quiz).all()
        serializer = AddQuizQuestionExplanSerializer(questions, many=True)
        return Response(serializer.data)

class TeacherQuizesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a teacher")

        quizes = QuizTeacherExplan.objects.filter(Teacher=teacher, Classes=myclass).all()
        mytime = datetime.datetime.now()
        serializer = TeacherQuizExplanSerializer(quizes, many=True)
        return Response(serializer.data)

class StartQuizView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacherExplan.objects.filter(Teacher=teacher, id=request.data['id']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("this quiz is already started")
        if quiz is not None:
            quiz.OpenTime=request.data['OpenTime']
            quiz.DurationHour=request.data['DurationHour']
            quiz.DurationMinute=request.data['DurationMinute']
            quiz.Is_Published=True
            quiz.save()
            return Response({'message':'Your quiz is visible to Students now'})
        else:
            return Response({'Error':'There is no such a quiz'})

class StudentQuizView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("there is no such a student")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("there is no such a student")

        quizzes = QuizTeacherExplan.objects.filter(Classes=myclass, Is_Published=True).all()
        serializer = TeacherQuizExplanSerializer(quizzes, many=True)
        return Response(serializer.data)

class StudentAnswerQuestion(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()



        ans = request.data['StudentAnswer']
        question = QuizQuestionExplan.objects.filter(id=request.data['QuizQuestionExplan_ID']).first()

        quizteacher = question.QuizTeacherExplan
        if not quizteacher:
            raise AuthenticationFailed("There is no such a quiz")

        obj = QuizStudentRecordExplan.objects.filter(Student=student, QuizTeacherExplan=quizteacher).first()
        if obj:
            raise AuthenticationFailed("You have already finished your exam")


        if not question:
            raise AuthenticationFailed("There is no such a question")
        obj = QuizQuestionStudentExplan.objects.filter(QuizQuestionExplan=question, Student=student).first()
        if not obj:
            obj2 = QuizQuestionStudentExplan.objects.create(QuizQuestionExplan=question, Student=student, StudentAnswer=ans)
            obj2.save()
            return Response({'message':'Your answer is submitted'})
        obj.StudentAnswer=ans
        obj.save()
        return Response({'message':'Your answer is changed'})

class StudentShowQuestions(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if not student:
            raise AuthenticationFailed("No such a student")
        quizteacher = QuizTeacherExplan.objects.filter(pk=request.data['QuizTeacherExplan']).first()
        if not quizteacher:
            raise AuthenticationFailed("There is no such a quiz")
        questions = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quizteacher).all()
        serializer = StudentQuestionExplanSerializer(questions, many=True)
        return Response(serializer.data)

class TeacherWatchRecords(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        quiz = QuizTeacherExplan.objects.filter(pk=request.data['QuizTeacherExplan_ID'], Teacher=teacher).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")
        records = QuizStudentRecordExplan.objects.filter(QuizTeacherExplan=quiz).all()
        serializer = StudentQuizRecordExplanSerializer(records, many=True)
        return Response(serializer.data)


class StudentfinishExam(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")

        quizteacher = QuizTeacherExplan.objects.filter(id=request.data['QuizTeacherExplan_ID']).first()
        if not quizteacher:
            raise AuthenticationFailed("There is no such a quiz")

        obj = QuizStudentRecordExplan.objects.filter(Student=student, QuizTeacherExplan=quizteacher).first()
        if obj:
            raise AuthenticationFailed("You have already finished your exam")
        # questions = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quizteacher).all()
        # correct = 0
        # whole = 0
        # for question in questions:
        #     checkThis = QuizQuestionStudent.objects.filter(Student=student, QuizQuestion=question).first()
        #
        #     whole += 1
        #     if not checkThis:
        #         continue
        #     if checkThis.StudentAnswer == question.Answer:
        #         correct += 1

        # deg = float(correct / whole)
        # deg = deg * 100
        now1 = datetime.datetime.now()
        q = QuizStudentRecordExplan.objects.create(FinishTime=now1, QuizTeacherExplan=quizteacher, Student = student,
                                                   Degree100=0,DegreeBarom=0)
        q.save()
        resp1 = Response()
        resp1.data = {
            'message': 'You have finished your exam.'
        }
        return resp1

class StudentExtraFinish(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")

        token = request.COOKIES.get('class')
        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(pk=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        records = QuizStudentRecordExplan.objects.filter(QuizTeacherExplan__Classes=myclass, Student=student).all()
        serializer = StudentQuizRecordExplanSerializer(records, many=True)
        return Response(serializer.data)

class RecordToStudent(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        record = QuizStudentRecordExplan.objects.filter(id=request.data['QuizStudentRecordExplan_ID']).first()
        if not record:
            raise AuthenticationFailed("There is no such a record")
        student = record.Student
        if not student:
            raise AuthenticationFailed("There is no such a student")
        serializer = StudentSerializer(student)
        return Response(serializer.data)

class StudentShowRecord(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")
        quiz = QuizTeacherExplan.objects.filter(id=request.data['QuizTeacherExplan_ID']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")
        noww = datetime.datetime.now()
        validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
        if noww < quiz.OpenTime:
            raise AuthenticationFailed("Exam is not started yet")
        if noww > validAfter:
            records = QuizStudentRecordExplan.objects.filter(QuizTeacherExplan = quiz, Student=student).first()
            if not records:
                raise AuthenticationFailed("There is no such a record")
            if records.marked == 0:
                raise AuthenticationFailed("This record is not marked yet")
            serializer = StudentQuizRecordExplanSerializer(records)
            return Response(serializer.data)
        return Response({'message':'it is not valid to show your records'})

class TeacherWatchStudentAnswers(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        quizstudentanswers = QuizStudentRecordExplan.objects.filter(id=request.data['QuizStudentRecordExplan_ID']).first()
        if not quizstudentanswers:
            raise AuthenticationFailed("There is no such a record")
        nanay = QuizQuestionStudentExplan.objects.filter(Student=quizstudentanswers.Student,QuizQuestionExplan__QuizTeacherExplan=quizstudentanswers.QuizTeacherExplan).all()
        serializer = QuizQuestionStudentExplanSerializer(nanay, many=True)
        return Response(serializer.data)

class TeacherFinishMark(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        quizstudentanswers = QuizStudentRecordExplan.objects.filter(id=request.data['QuizStudentRecordExplan_ID']).first()
        if not quizstudentanswers:
            raise AuthenticationFailed("There is no such a record")
        mybarom = QuizQuestionStudentExplan.objects.filter(Student=quizstudentanswers.Student,QuizQuestionExplan__QuizTeacherExplan=quizstudentanswers.QuizTeacherExplan).all()
        mynum = 0.0
        final = 0.0
        for c in mybarom:
            mynum += c.Correctness
            final += c.QuizQuestionExplan.Zarib
        percent = (mynum/final)*100
        quizstudentanswers.marked = 1
        quizstudentanswers.Degree100=percent
        quizstudentanswers.DegreeBarom=mynum
        quizstudentanswers.save()
        return Response({'message':'you have marked this student question completely'})

class TeacherMarkStudentAnswer(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        nanay = QuizQuestionStudentExplan.objects.filter(id=request.data['QuizQuestionStudentExplan_ID']).first()
        if not nanay:
            raise AuthenticationFailed("There is no such a question student side")
        cr = request.data['Correctness']
        if cr < 0 or cr > nanay.QuizQuestionExplan.Zarib:
            raise AuthenticationFailed("Wrong amount of Correctness")
        nanay.Correctness = cr
        nanay.save()
        return Response({'message':'you marked this student question'})

class QuizQuestionStudentView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")

        token = request.COOKIES.get('class')
        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(pk=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        quiz = QuizTeacherExplan.objects.filter(id=request.data['QuizTeacherExplan_ID']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")

        studentAnswers = QuizQuestionStudentExplan.objects.filter(QuizQuestionExplan__QuizTeacherExplan=quiz, Student=student).all()
        serializer = QuizQuestionStudentExplanSerializer(studentAnswers, many=True)
        return Response(serializer.data)

class StudentShowAnswers(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a teacher")
        # quiz2 = QuizStudent.objects.filter(Student=student, id=request.data['QuizStudent_ID']).first()
        quiz = QuizTeacherExplan.objects.filter(id=request.data['QuizTeacherExplan_ID']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")

        noww = datetime.datetime.now()
        validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
        if noww > validAfter:
            questions = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quiz).all()
            serializer = AddQuizQuestionExplanSerializer(questions, many=True)
            return Response(serializer.data)
        return Response({'message':'it is not valid to show you the answers'})


class QuizFinishedBoolean(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")

        token = request.COOKIES.get('class')
        if not token:
            raise AuthenticationFailed("Unauthenticated!!!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(pk=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        quiz = QuizTeacherExplan.objects.filter(id=request.data['QuizTeacherExplan_ID']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")

        qs = QuizStudentRecordExplan.objects.filter(QuizTeacherExplan=quiz, Student=student).first()
        if not qs:
            return Response({'boolean':False})
        return Response({'boolean':True})

class StudentShowDegree(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")
        # quiz2 = QuizStudent.objects.filter(Student=student, id=request.data['QuizStudent_ID']).first()
        quiz = QuizTeacherExplan.objects.filter(id=request.data['QuizTeacherExplan_ID']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")

        noww = datetime.datetime.now()
        validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
        if noww > validAfter:
            questions = QuizQuestionExplan.objects.filter(QuizTeacherExplan=quiz).all()
            serializer = AddQuizQuestionExplanSerializer(questions, many=True)
            return Response(serializer.data)
        return Response({'message':'it is not valid to show you the answers'})

