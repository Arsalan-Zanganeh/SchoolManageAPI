from http.client import responses

from django.contrib.sessions.models import Session
from django.core.serializers import serialize
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, StudentSerializer, TeacherSerializer, SchoolSerializer,SchoolProfileCompleteSerializer, SchoolProfileHalfSerializer,SchoolProfileOnlySerializer,ClassSerializer,ClassStudentSerializer, UserProfileCompleteSerializer, UserProfileHalfSerializer, UserProfileOnlySerializer
from .models import User, School, Classes, Teacher, ClassStudent, Student, UserProfile, SchoolProfile
from django.db.models import F
import jwt, datetime



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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
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

        serializer = TeacherSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        serializer = UserProfileCompleteSerializer(user)
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
        prof = UserProfile.objects.filter(user=user).first()
        serializer1 = UserProfileHalfSerializer(instance=user, data=request.data)
        serializer2 = UserProfileOnlySerializer(instance=prof, data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer2.is_valid(raise_exception=True)
        serializer1.save()
        serializer2.save()
        serializer = UserProfileCompleteSerializer(user)
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
        token = request.COOKIES.get('school')#school

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        prof = SchoolProfile.objects.filter(school=school).first()
        serializer1 = SchoolProfileHalfSerializer(instance=school, data=request.data)
        serializer2 = SchoolProfileOnlySerializer(instance=prof, data=request.data)
        serializer1.is_valid(raise_exception=True)
        serializer2.is_valid(raise_exception=True)
        serializer1.save()
        serializer2.save()
        serializer = SchoolProfileCompleteSerializer(school)
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow(),
        }

        token = jwt.encode(payload, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                           algorithm='HS256')

        response = Response()

        # response.set_cookie(key='school', value=token, httponly=True)
        response.set_cookie(key='school', value=token, httponly=True, samesite='None', secure=True)
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
        serializer = ClassSerializer(data=mydata)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
        serializer.save()
        return Response(serializer.data)

class ClassStudentView(APIView):
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


        students = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True).all()
        if not students:
            raise AuthenticationFailed("Student not found!")
        students2 = Student.objects.filter(National_ID__in=students).all()
        if not students2:
            raise AuthenticationFailed("Students not found!")

        serializer = StudentSerializer(students2, many=True)
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
