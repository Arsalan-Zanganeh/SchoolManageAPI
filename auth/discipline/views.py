from django.db.migrations import serializer
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import DisciplinaryScoreSerializer, DisciplinaryCaseSerializer, StudentSerializer, \
    StudentHomeworkSerializer
from users.models import DisciplinaryScore, User, School, DisciplinaryCase, Student, Teacher, Classes, HomeWorkStudent, \
     HomeWorkTeacher
import jwt, datetime
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

