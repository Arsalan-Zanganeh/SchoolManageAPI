from http.client import responses

from django.contrib.sessions.models import Session
from django.core.serializers import serialize
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import AbstractUser
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, SchoolSerializer, \
    SchoolProfileCompleteSerializer, SchoolProfileHalfSerializer, SchoolProfileOnlySerializer, \
    ClassSerializer, ClassStudentSerializer, UserProfileCompleteSerializer, UserProfileHalfSerializer, \
    UserProfileOnlySerializer, StudentProfileCompleteSerializer, StudentProfileHalfSerializer, \
    StudentProfileOnlySerializer, TeacherProfileOnlySerializer, TeacherProfileCompleteSerializer, \
    TeacherProfileHalfSerializer, StudentProfileCompleteViewSerializer, UserProfileCompleteViewSerializer, \
    TeacherProfileCompleteViewSerializer, NotificationStudentSerializer, NotificationSchoolSerializer, \
    ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer, CreateNewQuizSerializer, \
    TeacherQuizSerializer, StudentSetNewPasswordSerializer, \
    TeacherSetNewPasswordSerializer, AddQuizQuestionSerializer, StudentQuestionSerializer, StudentQuizRecordSerializer, \
    HallandAPISerializer, HomeWorkTeacherSerializer, HomeWorkStudentSerializer, PrinicipalCalendarSerializer, \
    QuizQuestionStudentSerializer, DisciplinaryScoreSerializer
from .models import User, School, Classes, Teacher, ClassStudent, Student, UserProfile, \
    SchoolProfile, StudentProfile, TeacherProfile, NotificationSchool, NotificationStudent, QuizTeacher, \
    QuizQuestion, QuizQuestionStudent, QuizStudentRecord, HallandAPI, HomeWorkTeacher, HomeWorkStudent, \
    PrinicipalCalendar, SchoolTeachers, DisciplinaryScore
from chat.models import AccountForChat
from chat.models import Chat
from django.db.models import F
import jwt, datetime
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,force_str,DjangoUnicodeDecodeError,smart_bytes
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

import datetime
import os.path
import webbrowser
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/calendar"]


# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.get(National_ID=request.data['National_ID'])
        prof = UserProfile.objects.create(user=user)
        prof.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        National_ID = request.data['National_ID']
        password = request.data['password']

        user = User.objects.filter(National_ID=National_ID).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password!")

        payload = {
            'National_ID': user.National_ID,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithm='HS256')

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        # response.set_cookie(key='jwt', value=token, httponly=True, samesite='None', secure=True)
        response.data = {
            'jwt': token
        }

        return response

class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have been logged out.'
        }

        return response

class AddStudentView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = request.COOKIES.get('school')

        if not school:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload2 = jwt.decode(school, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload2['Postal_Code']).first()

        if not school:
            raise AuthenticationFailed("School not found!")

        request.data['School']=school.pk
        serializer = StudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        student = Student.objects.filter(National_ID=request.data["National_ID"]).first()
        prof = StudentProfile.objects.create(student=student)
        prof.save()
        discip = DisciplinaryScore.objects.create(Student=student, Grade=100)
        discip.save()
        return Response(serializer.data)

class AddTeacherView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")
        payload = None
        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")
        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        if not school:
            raise AuthenticationFailed("School not found!")

        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        teacher = Teacher.objects.filter(National_ID=request.data['National_ID']).first()
        myobj = SchoolTeachers.objects.create(School=school, Teacher=teacher)
        myobj.save()
        return Response(serializer.data)

class AddSchoolView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()
        mydata = request.data
        mydata['Principal']=user.pk
        serializer = SchoolSerializer(data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class SchoolView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()
        schools = School.objects.filter(Principal=user).all()
        serializer = SchoolSerializer(schools, many=True)
        return Response(serializer.data)

class UserProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()
        serializer = UserProfileCompleteViewSerializer(user)
        return Response(serializer.data)

class UserProfileEditView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')#school

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()#user
        if request.data["Old_Password"]:
            if check_password(request.data["Old_Password"], user.password):
                user.password = make_password(request.data["New_Password"])
            else:
                raise AuthenticationFailed("Pass is not correct.")

        prof = UserProfile.objects.filter(user=user).first()
        serializer1 = UserProfileHalfSerializer(instance=user, data=request.data)
        serializer2 = UserProfileOnlySerializer(instance=prof, data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer2.is_valid(raise_exception=True)
        serializer1.save()
        serializer2.save()
        serializer = UserProfileCompleteSerializer(user)
        return Response(serializer.data)

class LoginSchoolView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()
        postal_code = request.data['Postal_Code']

        if user is None:
            raise AuthenticationFailed("User not found!")

        school = School.objects.filter(Postal_Code=postal_code, Principal=user).first()

        if school is None:
            raise AuthenticationFailed("School not found!")

        payload = {
            'Postal_Code': school.Postal_Code,
            'School_Name': school.School_Name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                           algorithm='HS256')

        response = Response()

        response.set_cookie(key='school', value=token, httponly=True)
        #response.set_cookie(key='school', value=token, httponly=True, samesite='None', secure=True)
        response.data = {
            'school': token
        }

        return response

class LogoutSchoolView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('school')
        response.data = {
            'message': 'Your School have been logged out.'
        }

        return response

class ClassView(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        if school is None:
            raise AuthenticationFailed("School not found!")

        classes = Classes.objects.filter(School=school).all()
        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)

class AddClassView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        mydata = request.data
        mydata['School'] = school.pk
        myteacher = Teacher.objects.filter(National_ID=mydata['National_ID']).first()
        mydata['Teacher']=myteacher.pk
        teacherAccount = AccountForChat.objects.filter(teacher=myteacher).first()
        if not teacherAccount:
            teacherAccount = AccountForChat.objects.create(teacher=myteacher, account_type="teacher")
        serializer = ClassSerializer(data=mydata)
        if serializer.is_valid(raise_exception=True):
            myClass = Classes.objects.create(Teacher=myteacher,Topic=request.data['Topic']
                        , Session1Day=request.data['Session1Day'], Session1Time=request.data['Session1Time']
                        , Session2Day=request.data['Session2Day'], Session2Time=request.data['Session2Time']
                        , School = school)
            #myClass.save()
        
            # Retrieve the validated data
            validated_data = serializer.validated_data
            # Fetch the class instance using the validated `id`
            myChat = Chat.objects.create(classes=myClass, title=Classes.Topic)
            myChat.save()
            myChat.participants.add(teacherAccount)
        return Response(serializer.data)

class EditClassView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        mydata = request.data
        mydata['School']=school.pk
        myclass = Classes.objects.filter(School=school,pk=mydata['id']).first()

        if mydata['Teacher']:
            teacher = Teacher.objects.filter(National_ID=mydata['Teacher']).first()
            mydata['Teacher'] = teacher.pk
        else:
            mydata['Teacher'] = myclass.Teacher.pk

        if mydata['Topic']:
            myclass.Topic = mydata['Topic']
        else:
            mydata['Topic'] = myclass.Topic

        if mydata['Session1Day']:
            myclass.Session1Day = mydata['Session1Day']
        else:
            mydata['Session1Day'] = myclass.Session1Day

        if mydata['Session2Day']:
            myclass.Session2Day = mydata['Session2Day']
        else:
            mydata['Session2Day'] = myclass.Session2Day

        if mydata['Session1Time']:
            myclass.Session1Time = mydata['Session1Time']
        else:
            mydata['Session1Time'] = myclass.Session1Time

        if mydata['Session2Time']:
            myclass.Session2Time = mydata['Session2Time']
        else:
            mydata['Session2Time'] = myclass.Session2Time

        serializer = ClassSerializer(instance=myclass, data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class DeleteClassView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        myclass = Classes.objects.filter(School=school,pk=request.data['id']).first()

        if not myclass:
            raise AuthenticationFailed("Class not found!")

        myclass.delete()
        response = Response()
        response.data = {
            'message': 'Your Class has been deleted.'
        }

        return response

class AddClassStudentView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        myclass = Classes.objects.filter(School=school,pk=request.data['Classes']).first()
        student = Student.objects.filter(National_ID=request.data['Student'],School=school).first()
        if not myclass:
            raise AuthenticationFailed("Class not found!")
        if not student:
            raise AuthenticationFailed("Student not found!")
        request.data['Student'] = student.pk
        serializer = ClassStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        myAccount = AccountForChat.objects.filter(student=student, account_type="student").first()
        if not myAccount:
            myAccount = AccountForChat.objects.create(student=student, account_type="student")
        myAccount.save()
        myChat = Chat.objects.filter(classes=myclass).first()
        myAccount2 = AccountForChat.objects.filter(student=student).first()
        myChat.participants.add(myAccount2)
        serializer.save()
        return Response(serializer.data)


class ClassStudentView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(
                token,
                'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                algorithms=['HS256']
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        if not school:
            return Response({"detail": "School not found"}, status=404)

        myclass = Classes.objects.filter(School=school, pk=request.data.get('id')).first()
        if not myclass:
            return Response({"detail": "Class not found"}, status=404)

        # Fetch students related to the class
        students = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True)
        if not students.exists():
            return Response([], status=200)  # Return an empty list if no students are found.

        students_data = Student.objects.filter(National_ID__in=students)
        serializer = StudentSerializer(students_data, many=True)
        return Response(serializer.data)

class TeacherClassStudentView(APIView):
    def post(self, request):

        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()

        myclass = Classes.objects.filter(Teacher=teacher, pk=request.data.get('id')).first()
        if not myclass:
            return Response({"detail": "Class not found"}, status=404)

        # Fetch students related to the class
        students = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True)
        if not students.exists():
            return Response([], status=200)  # Return an empty list if no students are found.

        students_data = Student.objects.filter(National_ID__in=students)
        serializer = StudentSerializer(students_data, many=True)
        return Response(serializer.data)

class DeleteClassStudentView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        myclass = Classes.objects.filter(School=school,pk=request.data['id']).first()
        student = Student.objects.filter(National_ID=request.data['Student'],School=school).first()

        if not myclass:
            raise AuthenticationFailed("Class not found!")

        if not student:
            raise AuthenticationFailed("Student not found!")

        obj = ClassStudent.objects.filter(Classes=myclass,Student=student).first()
        if not obj:
            raise AuthenticationFailed("This Student is not in the class!")

        obj.delete()
        response = Response()
        response.data = {
            'message': 'Your Student has been removed from class.'
        }

        return response
class StudentProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        serializer = StudentProfileCompleteViewSerializer(student)
        return Response(serializer.data)

class StudentProfileEditView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()

        if request.data["Old_Password"]:
            if check_password(request.data["Old_Password"], student.password):
                student.password = make_password(request.data["New_Password"])
            else:
                raise AuthenticationFailed("Pass is not correct.")


        prof = StudentProfile.objects.filter(student=student).first()
        serializer1 = StudentProfileHalfSerializer(instance=student, data=request.data)
        serializer2 = StudentProfileOnlySerializer(instance=prof, data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer2.is_valid(raise_exception=True)
        serializer1.save()
        serializer2.save()
        serializer = StudentProfileCompleteSerializer(student)



        return Response(serializer.data)
class TeacherProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        serializer = TeacherProfileCompleteViewSerializer(teacher)
        return Response(serializer.data)

class TeacherProfileEditView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()

        if request.data["Old_Password"]:
            if check_password(request.data["Old_Password"], teacher.password):
                teacher.password = make_password(request.data["New_Password"])
            else:
                raise AuthenticationFailed("Pass is not correct.")


        prof = TeacherProfile.objects.filter(teacher=teacher).first()
        serializer1 = TeacherProfileHalfSerializer(instance=teacher, data=request.data)
        serializer2 = TeacherProfileOnlySerializer(instance=prof, data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer2.is_valid(raise_exception=True)
        serializer1.save()
        serializer2.save()
        serializer = TeacherProfileCompleteSerializer(teacher)



        return Response(serializer.data)
class SchoolProfileView(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        serializer = SchoolProfileCompleteSerializer(school)
        return Response(serializer.data)

class SchoolProfileEditView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        if request.data["Old_Password"]:
            if check_password(request.data["Old_Password"], school.password):
                school.password = make_password(request.data["New_Password"])
            else:
                raise AuthenticationFailed("Pass is not correct.")


        prof = SchoolProfile.objects.filter(school=school).first()
        serializer1 = SchoolProfileHalfSerializer(instance=school, data=request.data)
        serializer2 = SchoolProfileOnlySerializer(instance=prof, data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer2.is_valid(raise_exception=True)
        serializer1.save()
        serializer2.save()
        serializer = SchoolProfileCompleteSerializer(school)



        return Response(serializer.data)



class NotificationSchoolView(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        token = request.COOKIES.get('jwt')#school

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload2 = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload2['National_ID']).first()
        if not user:
            raise AuthenticationFailed("User not Found!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        notif = NotificationSchool.objects.filter(school=school, archive=False).all()
        serializer = NotificationSchoolSerializer(notif, many=True)
        return Response(serializer.data)

class NotificationAddView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()

        token = request.COOKIES.get('jwt')#school

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = User.objects.filter(National_ID=payload['National_ID']).first()
        if not user:
            raise AuthenticationFailed("User not Found!")

        mynotif_sch = NotificationSchool.objects.create(school=school, message=request.data['message'])
        mynotif_sch.save()

        # first = {}
        # first['classes'] = Classes.objects.filter(pk=request.data['classes']).first().pk
        # if not first['classes']:
        #     raise AuthenticationFailed("No classes found!")
        #
        # first['NotificationSchool'] = mynotif_sch.pk
        # if not first['NotificationSchool']:
        #     raise AuthenticationFailed("Object NotificationSchool not found!")
        # serializer = NotificationClassSerializer(data=first)
        # serializer.is_valid(raise_exception=True)
        # serializer.save()

        first = {}
        first['NotificationSchool'] = mynotif_sch.pk
        first['seen']=False
        first['archive']=False
        first['message']= request.data['message']
        first['date']=mynotif_sch.date
        students = Student.objects.filter(School=school).all()
        for student in students:
            first['student'] = student.pk
            serializer = NotificationStudentSerializer(data=first)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        resp = Response()
        resp.data = {
            'message': 'It was successful'
        }
        return resp

class NotificationStudentView(APIView):
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
            raise AuthenticationFailed("Student not found!")
        notif = NotificationStudent.objects.filter(student=student, archive=False).all()
        # for notific in notif:
        #     notific.seen=True
        #     notific.save()
        serializer = NotificationStudentSerializer(notif, many=True)
        return Response(serializer.data)

class NotificationStudentSingleSeen(APIView):
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
            raise AuthenticationFailed("Student not found!")
        notif = NotificationStudent.objects.filter(student=student, archive=False, pk=request.data['id']).first()
        if not notif:
            raise AuthenticationFailed("notif not found!")
        notif.seen=True
        notif.save()
        return Response({'message':'you have seen your message'})

class NotificationUnseenCountStudentView(APIView):
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
            raise AuthenticationFailed("Student not found!")
        notif = NotificationStudent.objects.filter(student=student, archive=False, seen=False).count()
        resp = Response()
        resp.data = {
            "count": notif
        }
        return resp


class RequestPasswordResetEmailView(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        nid = request.data['National_ID']

        if User.objects.filter(email=email, National_ID=nid).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)

            # Generate the frontend URL with uidb64 and token
            absurl = f'http://localhost:5173/PasswordResetAdmin/{uidb64}/{token}/'
            email_body = f"Hello,\n\nPlease use the link below to reset your password:\n{absurl}"
            data = {
                'email_body': email_body,
                'to_email': user.email,
                'email_subject': 'Reset your password'
            }

            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'})
        else:
            return Response({'fail': 'There is no such user'})


class PasswordTokenCheckAPI(APIView):
    def get(self, request, uibd64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uibd64))
            user=User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Invalid request, please request a new one'})
            return Response({'success': True, 'message': 'Credentials Valid', 'uibd64': uibd64, 'token': token})
        except DjangoUnicodeDecodeError as e:
            return Response({'error': 'Invalid request, please request a new one'})


class SetNewPasswordAPIView(APIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'success': True, 'message': 'Your password has been set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentRequestPasswordResetEmailView(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        nid = request.data['National_ID']
        if Student.objects.filter(Email=email, National_ID=nid).exists():
            student = Student.objects.get(Email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(student.id))
            token = PasswordResetTokenGenerator().make_token(student)

            # Generate the frontend URL with uidb64 and token
            absurl = f'http://localhost:5173/PasswordResetStudent/{uidb64}/{token}/'
            email_body = f"Hello,\n\nPlease use the link below to reset your password:\n{absurl}"
            data = {
                'email_body': email_body,
                'to_email': student.Email,
                'email_subject': 'Reset your password'
            }

            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'})
        else:
            return Response({'fail': 'There is no such student'})


class StudentSetNewPasswordAPIView(APIView):
    serializer_class = StudentSetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Your password has been set'})

class StudentPasswordTokenCheckAPI(APIView):
    def get(self, request, uibd64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uibd64))
            student=Student.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(student, token):
                return Response({'error':'Invalid request, please request a new one'})
            return Response({'success': True, 'message': 'Credentials Valid', 'uibd64': uibd64, 'token': token})
        except DjangoUnicodeDecodeError as e:
            return Response({'error': 'Invalid request, please request a new one'})

####
class TeacherRequestPasswordResetEmailView(APIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        data = {'request': request, 'data': request.data}
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        nid = request.data['National_ID']

        if Teacher.objects.filter(Email=email, National_ID=nid).exists():
            teacher = Teacher.objects.get(Email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(teacher.id))
            token = PasswordResetTokenGenerator().make_token(teacher)

            # Generate the frontend URL with uidb64 and token
            absurl = f'http://localhost:5173/PasswordResetTeacher/{uidb64}/{token}/'
            email_body = f"Hello,\n\nPlease use the link below to reset your password:\n{absurl}"
            data = {
                'email_body': email_body,
                'to_email': teacher.Email,
                'email_subject': 'Reset your password'
            }

            Util.send_email(data)
            return Response({'success': 'We have sent you a link to reset your password'})
        else:
            return Response({'fail': 'There is no such teacher'})


class TeacherSetNewPasswordAPIView(APIView):
    serializer_class = TeacherSetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True,'message':'Your password has been set'})

class TeacherPasswordTokenCheckAPI(APIView):
    def get(self, request, uibd64, token):
        try:
            id=smart_str(urlsafe_base64_decode(uibd64))
            teacher=Teacher.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(teacher, token):
                return Response({'error':'Invalid request, please request a new one'})
            return Response({'success': True, 'message': 'Credentials Valid', 'uibd64': uibd64, 'token': token})
        except DjangoUnicodeDecodeError as e:
            return Response({'error': 'Invalid request, please request a new one'})

### Quiz

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

        myquiz = QuizTeacher.objects.create(Title=request.data['Title'], Teacher=teacher, Classes=myclass,
                                   OpenTime=datetime.datetime.now() + datetime.timedelta(days=1),
                                   DurationHour=0, DurationMinute=0)
        myquiz.save()
        serializer = CreateNewQuizSerializer(myquiz)
        return Response(serializer.data)

class AddQuizQuestionView(APIView):
    def post(selfself, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacher.objects.filter(Teacher=teacher, id=request.data['QuizTeacher']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("You can not change this quiz")
        if not (0<request.data['Answer']<5):
            raise AuthenticationFailed("Invalid Answer")
        question = QuizQuestion.objects.create(QuizTeacher=quiz, Question=request.data['Question'],
                                              Option1=request.data['Option1'],Option2=request.data['Option2'],
                                              Option3=request.data['Option3'],Option4=request.data['Option4'],
                                              Answer=request.data['Answer'],Explanation=request.data['Explanation'])
        question.save()
        return Response({'message':'Your question has been added'})

class DeleteQuizQuestionView(APIView):
    def post(selfself, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacher.objects.filter(Teacher=teacher, id=request.data['QuizTeacher']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("You can not change this quiz")
        question = QuizQuestion.objects.filter(QuizTeacher=quiz, pk=request.data['Question_ID']).first()
        question.delete()
        return Response({'message':'Your question has been deleted'})

class EditQuizQuestionView(APIView):
    def post(selfself, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        quiz = QuizTeacher.objects.filter(Teacher=teacher, id=request.data['QuizTeacher']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        if quiz.Is_Published:
            raise AuthenticationFailed("You can not change this quiz")
        question = QuizQuestion.objects.filter(QuizTeacher=quiz, pk=request.data['Question_ID']).first()
        question.Question = request.data['Question']
        question.Answer=request.data['Answer']
        question.Explanation=request.data['Explanation']
        question.Option1=request.data['Option1']
        question.Option2=request.data['Option2']
        question.Option3=request.data['Option3']
        question.Option4=request.data['Option4']
        question.save()
        return Response({'message':'Your question has been edited'})

class QuizQuestionsTeacherView(APIView):
    def post(selfself, request):
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
        quiz = QuizTeacher.objects.filter(Teacher=teacher, id=request.data['QuizTeacher']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")
        questions = QuizQuestion.objects.filter(QuizTeacher=quiz).all()
        serializer = AddQuizQuestionSerializer(questions, many=True)
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

        quizes = QuizTeacher.objects.filter(Teacher=teacher, Classes=myclass).all()
        mytime = datetime.datetime.now()
        serializer = TeacherQuizSerializer(quizes, many=True)
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
        quiz = QuizTeacher.objects.filter(Teacher=teacher, id=request.data['id']).first()
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

        quizzes = QuizTeacher.objects.filter(Classes=myclass, Is_Published=True).all()
        serializer = TeacherQuizSerializer(quizzes, many=True)
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
        if ans<0 or ans>4:
            raise AuthenticationFailed("answer should be 1 to 4 or null(0)")
        question = QuizQuestion.objects.filter(id=request.data['QuizQuestion_ID']).first()

        quizteacher = question.QuizTeacher
        if not quizteacher:
            raise AuthenticationFailed("There is no such a quiz")

        obj = QuizStudentRecord.objects.filter(Student=student, QuizTeacher=quizteacher).first()
        if obj:
            raise AuthenticationFailed("You have already finished your exam")


        if not question:
            raise AuthenticationFailed("There is no such a question")
        obj = QuizQuestionStudent.objects.filter(QuizQuestion=question, Student=student).first()
        if not obj:
            obj2 = QuizQuestionStudent.objects.create(QuizQuestion=question, Student=student, StudentAnswer=ans)
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
        quizteacher = QuizTeacher.objects.filter(pk=request.data['QuizTeacher']).first()
        if not quizteacher:
            raise AuthenticationFailed("There is no such a quiz")
        questions = QuizQuestion.objects.filter(QuizTeacher=quizteacher).all()
        serializer = StudentQuestionSerializer(questions, many=True)
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
        quiz = QuizTeacher.objects.filter(pk=request.data['Quiz_ID'], Teacher=teacher).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")
        records = QuizStudentRecord.objects.filter(QuizTeacher=quiz).all()
        serializer = StudentQuizRecordSerializer(records, many=True)
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

        quizteacher = QuizTeacher.objects.filter(id=request.data['QuizTeacher']).first()
        if not quizteacher:
            raise AuthenticationFailed("There is no such a quiz")

        obj = QuizStudentRecord.objects.filter(Student=student, QuizTeacher=quizteacher).first()
        if obj:
            raise AuthenticationFailed("You have already finished your exam")
        questions = QuizQuestion.objects.filter(QuizTeacher=quizteacher).all()
        correct = 0
        whole = 0
        for question in questions:
            checkThis = QuizQuestionStudent.objects.filter(Student=student, QuizQuestion=question).first()

            whole += 1
            if not checkThis:
                continue
            if checkThis.StudentAnswer == question.Answer:
                correct += 1
        deg = float(correct / whole)
        deg = deg * 100
        now1 = datetime.datetime.now()
        q = QuizStudentRecord.objects.create(Degree=deg, FinishTime=now1, QuizTeacher=quizteacher, Student = student)
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

        records = QuizStudentRecord.objects.filter(QuizTeacher__Classes=myclass, Student=student).all()
        serializer = StudentQuizRecordSerializer(records, many=True)
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

        record = QuizStudentRecord.objects.filter(id=request.data['QuizStudentRecord_ID']).first()
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
        quiz = QuizTeacher.objects.filter(id=request.data['QuizTeacher_ID']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")
        noww = datetime.datetime.now()
        validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
        if noww < quiz.OpenTime:
            raise AuthenticationFailed("Exam is not started yet")
        if noww > validAfter:
            records = QuizStudentRecord.objects.filter(QuizTeacher = quiz, Student=student).first()
            if not records:
                raise AuthenticationFailed("There is no such a record")
            serializer = StudentQuizRecordSerializer(records)
            return Response(serializer.data)
        return Response({'message':'it is not valid to show your records'})

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

        quiz = QuizTeacher.objects.filter(id=request.data['QuizTeacher_ID']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")

        studentAnswers = QuizQuestionStudent.objects.filter(QuizQuestion__QuizTeacher=quiz, Student=student).all()
        serializer = QuizQuestionStudentSerializer(studentAnswers, many=True)
        return Response(serializer.data)

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

        quiz = QuizTeacher.objects.filter(id=request.data['QuizTeacher_ID']).first()
        if not quiz:
            raise AuthenticationFailed("There is no such a quiz")

        qs = QuizStudentRecord.objects.filter(QuizTeacher=quiz, Student=student).first()
        if not qs:
            return Response({'boolean':False})
        return Response({'boolean':True})

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
        quiz = QuizTeacher.objects.filter(id=request.data['QuizTeacher_ID']).first()
        if not quiz:
            raise AuthenticationFailed("No such a quiz")

        noww = datetime.datetime.now()
        validAfter = quiz.OpenTime + datetime.timedelta(hours=quiz.DurationHour, minutes=quiz.DurationMinute)
        if noww > validAfter:
            questions = QuizQuestion.objects.filter(QuizTeacher=quiz).all()
            serializer = AddQuizQuestionSerializer(questions, many=True)
            return Response(serializer.data)
        return Response({'message':'it is not valid to show you the answers'})

class HallandRecordsView(APIView):
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
            raise AuthenticationFailed("There is no such a student")

        myhall = HallandAPI.objects.filter(Student=student).all()
        serializer = HallandAPISerializer(myhall, many=True)
        return Response(serializer.data)

class HallandSubmitRecord(APIView):
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

        num = HallandAPI.objects.filter(Student=student).count()
        num = num+1
        myrecord = HallandAPI.objects.create(Student=student, OnParticipation=num, Realistic=request.data['Realistic'],
                                             Investigative=request.data['Investigative'], Artistic=request.data['Artistic'],
                                             Social=request.data['Social'], Enterprising=request.data['Enterprising'],
                                             Conventional=request.data['Conventional'])
        myrecord.save()
        serializer = HallandAPISerializer(myrecord)
        return Response(serializer.data)

class TeacherAddHomeWork(APIView):
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

        myclass = Classes.objects.filter(pk=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        mydata = request.data
        mydata['Teacher'] = teacher.pk
        mydata['Classes'] = myclass.pk
        serializer = HomeWorkTeacherSerializer(data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TeacherEditHomeWork(APIView):
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

        mydata = request.data
        myhomework = HomeWorkTeacher.objects.filter(id=request.data['Homework_ID']).first()
        if myhomework.Is_Published:
            raise AuthenticationFailed("this homework is already published")
        mydata['Classes']=myhomework.Classes.pk
        mydata['DeadLine'] = request.data['DeadLine']
        mydata['Description'] = request.data['Description']
        mydata['Title'] = request.data['Title']
        mydata['Teacher']=teacher.pk
        serializer = HomeWorkTeacherSerializer(myhomework, data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class TeacherDeleteHomeWork(APIView):
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

        if 'Homework_ID' not in request.data:
            return Response({"error": "Homework_ID not provided"}, status=400)

        homework_id = request.data['Homework_ID']
        myhomework = HomeWorkTeacher.objects.filter(Teacher=teacher, id=homework_id).first()
        if not myhomework:
            return Response({"error": "There is no such a homework"}, status=404)

        myhomework.delete()
        return Response({'message': 'Your homework was deleted successfully'}, status=200)


class TeacherPublishHomeWork(APIView):
    def post(selfself, request):
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

        myhomework = HomeWorkTeacher.objects.filter(id=request.data['Homework_ID']).first()
        if not myhomework:
            raise AuthenticationFailed("there is no such a homework")
        if myhomework.Is_Published:
            raise AuthenticationFailed("this homework is already published")
        myhomework.Is_Published = True
        myhomework.save()
        myclassStudents = ClassStudent.objects.filter(Classes=myhomework.Classes).all()
        for myclassStudent in myclassStudents:
            obj = HomeWorkStudent.objects.create(Student=myclassStudent.Student, HomeWorkTeacher=myhomework)
            obj.save()

        myschool = SchoolTeachers.objects.filter(Teacher=teacher).first()
        if not myschool:
            raise AuthenticationFailed("There is no teacher with this National_ID")
        school = myschool.School
        if not school:
            raise AuthenticationFailed("There is no such a school for this teacher")

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, "../media/profile_image/credentials.json")
        if not mymodel:
            # mymodel = PrinicipalCalendar.objects.create(School=school)
            # token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     credentials_path, SCOPES
            # )
            # creds = flow.run_local_server(port=0)
            # mymodel.is_valid=True
            # mymodel.save()
            # with open(token_path, "w") as token:
            #     token.write(creds.to_json())
            return Response({'message': 'Your homework is visible to students now'})
        elif not mymodel.is_valid:
            # token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            # flow = InstalledAppFlow.from_client_secrets_file(
            #     credentials_path, SCOPES
            # )
            # creds = flow.run_local_server(port=0)
            # mymodel.is_valid=True
            # mymodel.save()
            # with open(token_path, "w") as token:
            #     token.write(creds.to_json())
            return Response({'message': 'Your homework is visible to students now'})

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        try:
            # Initialize Google Calendar API service
            service = build("calendar", "v3", credentials=creds)
            # Refer to the Python quickstart on how to setup the environment:
            # https://developers.google.com/calendar/quickstart/python
            # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
            # stored credentials.
            pacific = pytz.timezone('Asia/Tehran')
            nanay = pacific.localize(myhomework.DeadLine)

            started = nanay - datetime.timedelta(hours=1)
            Strstarted = started.isoformat()
            Strended = nanay.isoformat()

            print(f"Start Time: {Strstarted}, End Time: {Strended}")

            emails = [{'email': student.Student.Email} for student in myclassStudents]
            for student in myclassStudents:
                print(student.Student.Email)

            event = {
                'summary': myhomework.Title,
                'description': myhomework.Description,
                'start': {
                    'dateTime': Strstarted,
                    'timeZone': 'Asia/Tehran',
                },
                'end': {
                    'dateTime': Strended,
                    'timeZone': 'Asia/Tehran',
                },
                'attendees': emails,
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 24 * 60},
                        {'method': 'popup', 'minutes': 10},
                    ],
                },
            }

            event = service.events().insert(calendarId='primary', body=event).execute()

            # # Call the Calendar API
            # now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
            # print("Getting the upcoming 10 events")
            # events_result = (
            #     service.events()
            #     .list(
            #         calendarId="primary",
            #         timeMin=now,
            #         maxResults=10,
            #         singleEvents=True,
            #         orderBy="startTime",
            #     )
            #     .execute()
            # )
            # events = events_result.get("items", [])
            #
            #
            # # Prints the start and name of the next 10 events
            # for event in events:
            #     start = event["start"].get("dateTime", event["start"].get("date"))
            #     print(start, event["summary"])
            # calendar_list = service.calendarList().list().execute()
            # primary_calendar = next((cal for cal in calendar_list['items'] if cal.get('primary')), None)
            # calendar_id = None
            # if primary_calendar:
            #     calendar_id =  primary_calendar['id']  # This is the calendar ID for the primary calendar
            # else:
            #     raise AuthenticationFailed("Primary calendar not found.")
            # calendar_url = f"https://calendar.google.com/calendar/u/0/r?cid="+str(calendar_id)
            # webbrowser.open(calendar_url)
            return Response({"message":"It was done successfully"})

        except:
            return Response({"message":"An error occurred"})

class TeacherAllHomeWorks(APIView):
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

        myclass = Classes.objects.filter(Teacher=teacher, id=payload['Class_ID']).first()
        if not myclass:
            raise AuthenticationFailed("There is no such a class")

        homeworks = HomeWorkTeacher.objects.filter(Teacher=teacher, Classes=myclass).all()
        serializer = HomeWorkTeacherSerializer(homeworks, many=True)
        return Response(serializer.data)

class TeacherEnterClass(APIView):
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

        payload = {
            'Class_ID': request.data['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithm='HS256')

        response = Response()

        response.set_cookie(key='class', value=token, httponly=True)
        # response.set_cookie(key='class', value=token, httponly=True, samesite='None', secure=True)
        response.data = {
            'class': token
        }

        return response

class StudentEnterClass(APIView):
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

        payload = {
            'Class_ID': request.data['id'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=120),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithm='HS256')

        response = Response()

        response.set_cookie(key='class', value=token, httponly=True)
        # response.set_cookie(key='class', value=token, httponly=True, samesite='None', secure=True)
        response.data = {
            'class': token
        }

        return response

class StudentSeeHomeworks(APIView):
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
            raise AuthenticationFailed("There is no such a student")

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

        homeworks = HomeWorkTeacher.objects.filter(Classes=myclass).all()
        serializer = HomeWorkTeacherSerializer(homeworks, many=True)
        return Response(serializer.data)

class StudentSendHomework(APIView):
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

        homeworkteacher = HomeWorkTeacher.objects.filter(id=request.data['Homework_ID']).first()
        nanay = HomeWorkStudent.objects.filter(HomeWorkTeacher=homeworkteacher, Student=student).first()
        if not nanay:
            studenthomework = HomeWorkStudent.objects.create(HomeWorkTeacher=homeworkteacher, Student=student,
                                                         SendingTime=datetime.datetime.now(),
                                                         HomeWorkAnswer=request.data['HomeWorkAnswer'])
            studenthomework.save()
            serializer = HomeWorkStudentSerializer(studenthomework)
            return Response(serializer.data)
        nanay.SendingTime = datetime.datetime.now()
        nanay.HomeWorkAnswer = request.data['HomeWorkAnswer']
        nanay.save()
        serializer = HomeWorkStudentSerializer(nanay)
        return Response(serializer.data)

class StudentSeeHomeworkRecords(APIView):
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

        homeworks = HomeWorkStudent.objects.filter(HomeWorkTeacher=request.data['Homework_ID']).all()
        serializer = HomeWorkStudentSerializer(homeworks, many=True)
        return Response(serializer.data)

class PrinicipalCalendarView(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        if not school:
            raise AuthenticationFailed("There is no such a school")

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, "../media/profile_image/credentials.json")
        if not mymodel:
            mymodel = PrinicipalCalendar.objects.create(School=school)
            token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
            mymodel.is_valid=True
            mymodel.save()
            with open(token_path, "w") as token:
                token.write(creds.to_json())
        elif not mymodel.is_valid:
            token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES
            )
            creds = flow.run_local_server(port=0)
            mymodel.is_valid=True
            mymodel.save()
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(token_path, "w") as token:
                token.write(creds.to_json())

        try:
            # Initialize Google Calendar API service
            service = build("calendar", "v3", credentials=creds)

            # Call the Calendar API
            now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
            print("Getting the upcoming 10 events")
            events_result = (
                service.events()
                .list(
                    calendarId="primary",
                    timeMin=now,
                    maxResults=10,
                    singleEvents=True,
                    orderBy="startTime",
                )
                .execute()
            )
            events = events_result.get("items", [])


            # Prints the start and name of the next 10 events
            for event in events:
                start = event["start"].get("dateTime", event["start"].get("date"))
                print(start, event["summary"])
            calendar_list = service.calendarList().list().execute()
            primary_calendar = next((cal for cal in calendar_list['items'] if cal.get('primary')), None)
            calendar_id = None
            if primary_calendar:
                calendar_id =  primary_calendar['id']  # This is the calendar ID for the primary calendar
            else:
                raise AuthenticationFailed("Primary calendar not found.")
            calendar_url = f"https://calendar.google.com/calendar/u/0/r?cid="+str(calendar_id)
            webbrowser.open(calendar_url)
            return Response({"message":"It was done successfully"})

        except:
            return Response({"message":"An error occurred"})

class StudentCalendarView(APIView):
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
            raise AuthenticationFailed("There is no such a school")

        school = student.School
        if not school:
            raise AuthenticationFailed("This student has no school")
        mymodel = PrinicipalCalendar.objects.filter(School=school).first()
        current_dir = os.path.dirname(os.path.abspath(__file__))
        credentials_path = os.path.join(current_dir, "../media/profile_image/credentials.json")
        if not mymodel:
            return Response({'message':'There is no related calendar to your school'})
        else:
            token_path = os.path.join(current_dir, "../media", str(mymodel.gtoken))
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)

            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
                with open(token_path, "w") as token:
                    token.write(creds.to_json())

            try:
                # Initialize Google Calendar API service
                service = build("calendar", "v3", credentials=creds)

                # Call the Calendar API
                now = datetime.datetime.now().isoformat() + "Z"  # 'Z' indicates UTC time
                print("Getting the upcoming 10 events")
                events_result = (
                    service.events()
                    .list(
                        calendarId="primary",
                        timeMin=now,
                        maxResults=10,
                        singleEvents=True,
                        orderBy="startTime",
                    )
                    .execute()
                )
                events = events_result.get("items", [])

                # Prints the start and name of the next 10 events
                for event in events:
                    start = event["start"].get("dateTime", event["start"].get("date"))
                    print(start, event["summary"])
                calendar_list = service.calendarList().list().execute()
                primary_calendar = next((cal for cal in calendar_list['items'] if cal.get('primary')), None)
                calendar_id = None
                if primary_calendar:
                    calendar_id =  primary_calendar['id']  # This is the calendar ID for the primary calendar
                else:
                    raise AuthenticationFailed("Primary calendar not found.")
                calendar_url = f"https://calendar.google.com/calendar/embed?src={calendar_id}&mode=AGENDA"
                webbrowser.open(calendar_url)
                return Response({"message":"It was done successfully"})

            except:
                return Response({"message":"An error occurred"})

class SchoolTeachersView(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        teachers = SchoolTeachers.objects.filter(School=school).values_list('Teacher__National_ID', flat=True)
        teachers_data = Teacher.objects.filter(National_ID__in=teachers).all()
        serializer = TeacherSerializer(teachers_data, many=True)
        return Response(serializer.data)

class TeacherIdtoInfo(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        student = Student.objects.filter(National_ID=payload['National_ID']).first()
        principal = User.objects.filter(National_ID=payload['National_ID']).first()
        if (not student) and (not principal):
            raise AuthenticationFailed("You should be at least a student or principal to view this")

        teacher = Teacher.objects.filter(id=request.data['id']).first()
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)
