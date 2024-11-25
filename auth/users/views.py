from http.client import responses

from django.contrib.sessions.models import Session
from django.core.serializers import serialize
from django.contrib.auth.hashers import check_password, make_password
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
    NotificationClassSerializer
from .models import User, School, Classes, Teacher, ClassStudent, Student, UserProfile, \
    SchoolProfile, StudentProfile, TeacherProfile, NotificationSchool, NotificationStudent
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
        student = Student.objects.filter(National_ID=request.data["National_ID"]).first()
        prof = StudentProfile.objects.create(student=student)
        prof.save()
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
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

        first = {}
        first['classes'] = Classes.objects.filter(pk=request.data['classes']).first().pk
        if not first['classes']:
            raise AuthenticationFailed("No classes found!")

        first['NotificationSchool'] = mynotif_sch.pk
        if not first['NotificationSchool']:
            raise AuthenticationFailed("Object NotificationSchool not found!")
        serializer = NotificationClassSerializer(data=first)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        first = {}
        first['NotificationSchool'] = mynotif_sch.pk
        first['seen']=False
        first['archive']=False
        first['message']= request.data['message']
        first['date']=mynotif_sch.date
        myclasses = ClassStudent.objects.filter(Classes=request.data['classes']).values_list('Student__National_ID', flat=True)
        students = Student.objects.filter(National_ID__in=myclasses).all()
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
        for notific in notif:
            notific.seen=True
            notific.save()
        serializer = NotificationStudentSerializer(notif, many=True)
        return Response(serializer.data)

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