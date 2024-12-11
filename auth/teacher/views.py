# Create your views here.
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
from users.serializers import TeacherSerializer, ClassSerializer, StudentSerializer, AttendanceFormSerializer
from users.models import Teacher, ClassStudent, Classes, Student, StudentAttendance
import jwt, datetime
from django.contrib.auth.hashers import make_password, check_password



# Create your views here.
class TeacherLoginView(APIView):
    def post(self, request):
        National_ID = request.data['National_ID']
        password = request.data['password']
        user = Teacher.objects.filter(National_ID=National_ID).first()

        if user is None:
            raise AuthenticationFailed("User not found!")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Wrong password!")

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

class TeacherView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        user = Teacher.objects.filter(National_ID=payload['National_ID']).first()
        serializer = TeacherSerializer(user)

        return Response(serializer.data)

class TeacherLogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'You have been logged out.'
        }

        return response

class TeacherClassesView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Teacher Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()

        classes = Classes.objects.filter(Teacher=teacher).all()
        if not classes:
            raise AuthenticationFailed("Class not found!")

        serializer = ClassSerializer(classes, many=True)
        return Response(serializer.data)


class TeacherClassStudentsView(APIView):
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
            raise AuthenticationFailed("There is no teacher with this National_ID")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")


        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            return Response({"message":"There is no class with this National_ID"})

        students1 = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True)
        students2 = Student.objects.filter(National_ID__in=students1)
        serializer = StudentSerializer(students2, many=True)
        return Response(serializer.data)

class TeacherCheckStudentAttendance(APIView):
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
            raise AuthenticationFailed("There is no teacher with this National_ID")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")


        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            return Response({"message":"There is no class with this information"})

        student = Student.objects.filter(National_ID=request.data['National_ID']).first()
        if not student:
            raise AuthenticationFailed("There is no student with this National_ID")

        classStudent = ClassStudent.objects.filter(Classes=myclass, Student=student).first()
        if not classStudent:
            return Response({"message":"There is no class with this information"})

        myobj = StudentAttendance.objects.filter(ClassStudent=classStudent, Date=request.data['Date']).first()
        if not myobj:
            myobj2 = StudentAttendance.objects.create(ClassStudent=classStudent, Date=request.data['Date'], Absent=request.data['Absent'])
            myobj2.save()
        else:
            myobj.Absent = request.data['Absent']
            myobj.save()
        if request.data['Absent'] == True:
            return Response({"message":"Absent"})
        return Response({"message":"Present"})

class TeacherWatchAttendance(APIView):
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
            raise AuthenticationFailed("There is no teacher with this National_ID")

        token = request.COOKIES.get('class')

        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")


        myclass = Classes.objects.filter(id=payload['Class_ID']).first()
        if not myclass:
            return Response({"message":"There is no class with this information"})

        classStudent = ClassStudent.objects.filter(Classes=myclass).first()
        if not classStudent:
            return Response({"message":"There is no class with this information"})

        myobj = StudentAttendance.objects.filter(ClassStudent=classStudent, Date=request.data['Date']).first()
        if not myobj:
            myvals = ClassStudent.objects.filter(Classes=myclass).values_list('Student__National_ID', flat=True)
            students = Student.objects.filter(National_ID__in=myvals).all()
            for student in students:
                myclassStudent = ClassStudent.objects.filter(Classes=myclass, Student=student).first()
                myobj2 = StudentAttendance.objects.create(ClassStudent=myclassStudent, Date=request.data['Date'])
                myobj2.save()
            mydata = StudentAttendance.objects.filter(ClassStudent__Classes=myclass, Date=request.data['Date']).all()
            serializer = AttendanceFormSerializer(mydata, many=True)
            return Response(serializer.data)
        mydata = StudentAttendance.objects.filter(ClassStudent__Classes=myclass, Date=request.data['Date']).all()
        serializer = AttendanceFormSerializer(mydata, many=True)
        return Response(serializer.data)