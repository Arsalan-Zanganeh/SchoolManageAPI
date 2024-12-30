from django.shortcuts import render
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt, datetime
from users.models import School, User, Student, NotificationSchoolParent, NotificationParent
from users.serializers import NotificationParentSerializer, NotificationSchoolParentSerializer
# Create your views here.
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
        notif = NotificationSchoolParent.objects.filter(school=school, archive=False).all()
        serializer = NotificationSchoolParentSerializer(notif, many=True)
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

        mynotif_sch = NotificationSchoolParent.objects.create(school=school, message=request.data['message'])
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
            serializer = NotificationParentSerializer(data=first)
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
        notif = NotificationParent.objects.filter(student=student, archive=False).all()
        # for notific in notif:
        #     notific.seen=True
        #     notific.save()
        serializer = NotificationParentSerializer(notif, many=True)
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
        notif = NotificationParent.objects.filter(student=student, archive=False, pk=request.data['id']).first()
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
        notif = NotificationParent.objects.filter(student=student, archive=False, seen=False).count()
        resp = Response()
        resp.data = {
            "count": notif
        }
        return resp