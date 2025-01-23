from django.core.serializers import serialize
from django.shortcuts import render
from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime
from users.models import Teacher, Student, Classes, School, ClassStudent, StudentProfile, TeacherProfile

from users.serializers import StudentSerializer, TeacherSerializer, StudentPictureSerializer, TeacherPictureSerializer


# Create your views here.
class StudentFiles(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        students = Student.objects.filter(School=school).all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

class TeacherFiles(APIView):
    def get(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        classes = Classes.objects.filter(School=school).values_list('Teacher__National_ID', flat=True)
        teachers = Teacher.objects.filter(National_ID__in=classes).all()
        serializer = TeacherSerializer(teachers, many=True)
        return Response(serializer.data)

class FilterStudents(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        students = Student.objects.filter(School=school, Grade_Level=request.data['Grade_Level']).all()
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)


class StudentPictureTeacherSideView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school') or request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed("Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121',
                                 algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        if 'Postal_Code' in payload:
            school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
            if not school:
                raise AuthenticationFailed("School not found!")

        elif 'National_ID' in payload:
            teacher = Teacher.objects.filter(National_ID=payload['National_ID']).first()
            if not teacher:
                raise AuthenticationFailed("There is no teacher with this National_ID")

        students1 = Student.objects.filter(National_ID=request.data['National_ID']).first()
        if not students1:
            raise AuthenticationFailed("There is no student with this National_ID")

        profPic = StudentProfile.objects.filter(student=students1).first()
        if not profPic:
            return Response({"message": "No profile picture found for this student."}, status=404)

        serializer = StudentPictureSerializer(profPic)
        return Response(serializer.data)

class TeacherPicturePrincipalSideView(APIView):
    def post(self, request):
        token = request.COOKIES.get('school')
        if not token:
            raise AuthenticationFailed("School Unauthenticated!")

        try:
            payload = jwt.decode(token, 'django-insecure-7sr^1xqbdfcxes^!amh4e0k*0o2zqfa=f-ragz0x0v)gcqx121', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("Expired token!")

        school = School.objects.filter(Postal_Code=payload['Postal_Code']).first()
        teacher = Teacher.objects.filter(National_ID=request.data['National_ID']).first()
        if not teacher:
            raise AuthenticationFailed("There is no teacher with this National_ID")
        picProf = TeacherProfile.objects.filter(teacher=teacher).first()
        serializer = TeacherPictureSerializer(picProf)
        return Response(serializer.data)