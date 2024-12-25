from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import DisciplinaryScoreSerializer, DisciplinaryCaseSerializer, StudentSerializer, \
    StudentHomeworkSerializer, ECFileSerializer, ECVideoSerializer, StudentPlanningSerializer, TeacherFeedbackSerializer
from users.models import DisciplinaryScore, User, School, DisciplinaryCase, Student, Teacher, Classes, HomeWorkStudent, \
     HomeWorkTeacher, ECFile, ECVideo, StudentPlanning, TeacherFeedback
from chat.models import Chat
import jwt, datetime
import re
from django.contrib.auth.hashers import make_password, check_password


# Create your views here.

class DisciplineScoreList(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        students = DisciplinaryScore.objects.filter(Student__School=school).all()
        serializer = DisciplinaryScoreSerializer(students, many=True)
        return Response(serializer.data)

class DisciplineScoreChange(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        student = DisciplinaryScore.objects.filter(Student__National_ID=request.data['National_ID']).first()
        student.Grade=request.data['Grade']
        student.save()
        serializer = DisciplinaryScoreSerializer(student)
        return Response(serializer.data)

class DisciplinaryCaseList(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        student = DisciplinaryCase.objects.filter(Student__School=school).all()
        serializer = DisciplinaryCaseSerializer(student, many=True)
        return Response(serializer.data)

class DisciplinaryCaseAdd(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        mystudent = Student.objects.filter(National_ID=request.data['National_ID']).first()
        student = DisciplinaryCase.objects.create(Student=mystudent, Case=request.data['Case'])
        student.save()
        serializer = DisciplinaryCaseSerializer(student)
        return Response(serializer.data)

class DisciplinaryCaseDelete(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        student = DisciplinaryCase.objects.filter(id=request.data['id']).first()
        student.delete()
        return Response({'message':'your case was deleted successfully!'})

class StudentsofSchool(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        students = Student.objects.filter(School=school).all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class TeacherWatchStudentHomeworkAnswers(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")
        myhomworkteacher = HomeWorkTeacher.objects.filter(id=request.data['id']).first()
        if not myhomworkteacher:
            raise AuthenticationFailed("There is no such a homework teacher-side with this id")
        homeWorkStudent = HomeWorkStudent.objects.filter(HomeWorkTeacher=myhomworkteacher).all()
        serializer = StudentHomeworkSerializer(homeWorkStudent, many=True)
        return Response(serializer.data)

class TeacherAddChangeHomeworkGrade(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")
        student = Student.objects.filter(id=request.data['Student']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")
        teacherhomework = HomeWorkTeacher.objects.filter(id=request.data['id']).first()
        if not teacherhomework:
            raise AuthenticationFailed("There is no such a teacher-side homework")
        myhomeworkscore = HomeWorkStudent.objects.filter(Student=student,HomeWorkTeacher=teacherhomework).first()
        if not myhomeworkscore:
            myobj = HomeWorkStudent.objects.create(Student=student,HomeWorkTeacher=teacherhomework, Grade=request.data['Grade'])
            myobj.save()
            serializer = StudentHomeworkSerializer(myobj)
            return Response(serializer.data)
        myhomeworkscore.Grade = request.data['Grade']
        myhomeworkscore.Graded = True
        myhomeworkscore.save()
        serializer = StudentHomeworkSerializer(myhomeworkscore)
        return Response(serializer.data)

class TeacherAddFileEducationalContent(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECFile.objects.create(Classes=myclass, file=request.data['file'], Title=request.data['Title'])
        obj.save()
        serializer = ECFileSerializer(obj)
        return Response(serializer.data)

class TeacherDeleteFileEducationalContent(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECFile.objects.filter(id=request.data['id']).first()
        obj.delete()
        return Response({'message':'it was deleted successfully'})

class TeacherWatchFileEducationalContent(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECFile.objects.filter(Classes=myclass).all()
        serializer = ECFileSerializer(obj, many=True)
        return Response(serializer.data)

class TeacherAddVideoEducationalContent(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        pattern = r'^(https?://(www.)?youtube.com/embed/)'

        # Check if the URL matches the pattern
        valid_src = re.match(pattern, request.data['src'])
        if not valid_src:
            raise AuthenticationFailed("Invalid URL!")

        obj = ECVideo.objects.create(Classes=myclass, src=request.data['src'], Title=request.data['Title'])
        obj.save()
        serializer = ECVideoSerializer(obj)
        return Response(serializer.data)

class TeacherDeleteVideoEducationalContent(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECVideo.objects.filter(id=request.data['id']).first()
        obj.delete()
        return Response({'message':'it was deleted successfully'})

class TeacherWatchVideoEducationalContent(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECVideo.objects.filter(Classes=myclass).all()
        serializer = ECVideoSerializer(obj, many=True)
        return Response(serializer.data)

class StudentWatchVideoEducationalContent(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECVideo.objects.filter(Classes=myclass).all()
        serializer = ECVideoSerializer(obj, many=True)
        return Response(serializer.data)

class StudentWatchFileEducationalContent(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        obj = ECFile.objects.filter(Classes=myclass).all()
        serializer = ECFileSerializer(obj, many=True)
        return Response(serializer.data)

class StudentAddPlan(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")
        mydata = request.data
        mydata['Student']=student.pk
        serializer = StudentPlanningSerializer(data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class StudentWatchPlans(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")

        obj = StudentPlanning.objects.filter(Student=student).all()
        serializer = StudentPlanningSerializer(obj, many=True)
        return Response(serializer.data)

class StudentDeletePlan(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no such a student")
        obj = StudentPlanning.objects.filter(Student=student, id=request.data['id']).first()
        if not obj:
            raise AuthenticationFailed("There is no such a plan id with this student")
        obj.delete()
        return Response({'message':'the plan was deleted successfully'})

class TeacherWatchStudentPlans(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        obj = StudentPlanning.objects.filter(Student=request.data['Student_ID']).all()
        serializer = StudentPlanningSerializer(obj, many=True)
        return Response(serializer.data)

class TeacherAddStudentPlan(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        # obj = StudentPlanning.objects.filter(Student=request.data['Student_ID'])
        student = Student.objects.filter(id=request.data['Student_ID']).first()
        obj = StudentPlanning.objects.create(Student=student, StartDate=request.data['StartDate'],
                                             Title=request.data['Title'], Duration=request.data['Duration'],
                                             Explanation=request.data['Explanation'])
        obj.save()
        return Response({'message':'the plan was added successfully'})

class TeacherDeletePlan(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a student")
        obj = StudentPlanning.objects.filter(id=request.data['id']).first()
        if not obj:
            raise AuthenticationFailed("There is no such a plan id with this student")
        obj.delete()
        return Response({'message':'the plan was deleted successfully'})

class TeacherAddFeedback(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        plan = StudentPlanning.objects.filter(id=request.data['StudentPlanning_ID']).first()
        if not plan:
            raise AuthenticationFailed("There is no such a plan")
        plan.feedbackCount += 1
        plan.save()
        feedback = TeacherFeedback.objects.create(StudentPlanning=plan,
                                                  Teacher=teacher,
                                                  Feedback=request.data['Feedback'])

        feedback.save()
        serializer = TeacherFeedbackSerializer(feedback)
        return Response(serializer.data)

class TeacherDeleteFeedback(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no such a teacher")
        feedback = TeacherFeedback.objects.filter(id=request.data['TeacherFeedback_ID'], Teacher=teacher).first()
        if not feedback:
            raise AuthenticationFailed("There is no such a feedback")
        plan = feedback.StudentPlanning
        plan.feedbackCount -= 1
        plan.save()
        feedback.delete()
        return Response({'message':'feedback deleted'})

class TeacherWatchFeedbacks(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        if not teacher and not student:
            raise AuthenticationFailed("There is no such a teacher or student")
        plan = StudentPlanning.objects.filter(id=request.data['StudentPlanning_ID']).first()
        if not plan:
            raise AuthenticationFailed("There is no such a plan")
        feedback = TeacherFeedback.objects.filter(StudentPlanning=plan).all()
        serializer = TeacherFeedbackSerializer(feedback, many=True)
        return Response(serializer.data)

class WSGetID(APIView):
    def get(self, request):
        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        myChat = Chat.objects.filter(classes=myclass).first()
        return Response({"id":myChat.id})